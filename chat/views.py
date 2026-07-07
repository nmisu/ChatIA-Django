from django.db.models import Q
import os
import requests
import time
import concurrent.futures
import uuid
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from .models import Conversation, Message, Profile, SharedLink
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse

# Cargar variables de entorno
load_dotenv()

def request_ai_reply(historial_mensajes, modelo_elegido):
    """
    Función auxiliar para comunicarse con la API de NVIDIA NIM.
    Ahora recibe el modelo dinámicamente desde el desplegable.
    """
    token = os.environ.get('NVIDIA_API_KEY')
    endpoint = 'https://integrate.api.nvidia.com/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': modelo_elegido, 
        'messages': historial_mensajes,
        'max_tokens': 1024,
        'temperature': 0.7
    }

    try:
        # TIMEOUT AUMENTADO A 90 PARA DEEPSEEK
        res = requests.post(endpoint, headers=headers, json=payload, timeout=90)
        res.raise_for_status() 
        return res.json().get('choices')[0].get('message').get('content')
    except Exception as e:
        print(f"Error de conexión con NVIDIA NIM: {e}")
        return "Hubo un fallo al conectar con el asistente virtual (NVIDIA NIM)."

def support_page(request):
    return render(request, "chat/help.html")

def landing_view(request):
    """Página principal pública (sin decorador login_required)"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'chat/landing.html')

def register_view(request):
    """Página de registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'chat/register.html', {'form': form})

@login_required
def index_view(request):
    Profile.objects.get_or_create(user=request.user)
    
    # 1. Capturar la búsqueda (si existe)
    query = request.GET.get('q', '')
    
    # 2. Filtrado base
    conversations = Conversation.objects.filter(user=request.user)
    
    # 3. Lógica del buscador (busca en título O en el texto de los mensajes)
    if query:
        conversations = conversations.filter(
            Q(title__icontains=query) | Q(messages__content__icontains=query)
        ).distinct() # Distinct es vital para no duplicar chats
        
    # 4. Separamos activos de archivados y ordenamos
    active_chats = conversations.filter(is_archived=False).order_by('-is_pinned', '-created_at')
    archived_chats = conversations.filter(is_archived=True).order_by('-created_at')
    
    return render(request, 'chat/home.html', {
        'active_chats': active_chats,
        'archived_chats': archived_chats,
        'query': query
    })

@login_required
def toggle_pin_chat(request, conv_id):
    chat = get_object_or_404(Conversation, id=conv_id, user=request.user)
    chat.is_pinned = not chat.is_pinned
    chat.save()
    return redirect('home')

@login_required
def toggle_archive_chat(request, conv_id):
    chat = get_object_or_404(Conversation, id=conv_id, user=request.user)
    chat.is_archived = not chat.is_archived
    # Si lo archivamos, le quitamos la chincheta por lógica
    if chat.is_archived:
        chat.is_pinned = False 
    chat.save()
    return redirect('home')

@login_required
def user_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.alias = request.POST.get('alias', '')
        profile.theme = request.POST.get('theme', 'rosa')
        profile.save()
        return redirect('profile')
    return render(request, 'chat/profile.html', {'profile': profile})

@login_required
def new_chat_view(request):
    nuevo_chat = Conversation.objects.create(user=request.user, title="Nueva conversación")
    return redirect('conversation_detail', conv_id=nuevo_chat.id)

@login_required
def chat_detail_view(request, conv_id):
    current_chat = get_object_or_404(Conversation, id=conv_id, user=request.user)

    if request.method == 'POST':
        user_input = request.POST.get('content', '').strip()
        
        modelo_seleccionado = request.POST.get('ia_model', current_chat.ai_model)
        
        if current_chat.ai_model != modelo_seleccionado:
            current_chat.ai_model = modelo_seleccionado
            current_chat.save()
        
        if user_input:
            if current_chat.title == "Nueva conversación":
                current_chat.title = user_input[:30]
                current_chat.save()

            Message.objects.create(conversation=current_chat, role='user', content=user_input)
            
            mensajes_recientes = current_chat.messages.all().order_by('-created_at')[:10]
            historial_api = [
                {"role": m.role, "content": m.content} 
                for m in reversed(mensajes_recientes)
            ]
            
            ia_reply = request_ai_reply(historial_api, current_chat.ai_model)
            Message.objects.create(conversation=current_chat, role='assistant', content=ia_reply)

    chat_history = current_chat.messages.all().order_by('created_at')

    if request.headers.get('HX-Request'):
        return render(request, 'chat/messages.html', {'messages': chat_history})
        
    return render(request, 'chat/conversation_detail.html', {
        'conversation': current_chat, 
        'messages': chat_history
    })

@login_required
def update_chat_title(request, conv_id):
    chat_to_edit = get_object_or_404(Conversation, id=conv_id, user=request.user)
    if request.method == 'POST':
        updated_title = request.POST.get('title')
        if updated_title:
            chat_to_edit.title = updated_title
            chat_to_edit.save()
        return redirect('home')
    return render(request, 'chat/rename_conversation.html', {'conversation': chat_to_edit})

@login_required
def remove_chat(request, conv_id):
    chat_to_delete = get_object_or_404(Conversation, id=conv_id, user=request.user)
    chat_to_delete.delete()
    return redirect('home')

@login_required
def export_conversation_json(request, conv_id):
    chat_to_export = get_object_or_404(Conversation, id=conv_id, user=request.user)
    
    data = {
        "id_chat": chat_to_export.id,
        "titulo": chat_to_export.title,
        "fecha_creacion": chat_to_export.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        "usuario": request.user.username,
        "mensajes": []
    }
    
    for msg in chat_to_export.messages.all().order_by('created_at'):
        data["mensajes"].append({
            "rol": msg.role,
            "contenido": msg.content,
            "fecha": msg.created_at.strftime("%d/%m/%Y %H:%M:%S")
        })
        
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

def rate_message(request, message_id, action):
    message = get_object_or_404(Message, id=message_id)
    if message.conversation.user == request.user:
        if action == 'like':
            message.feedback = 1 if message.feedback != 1 else 0
        elif action == 'dislike':
            message.feedback = -1 if message.feedback != -1 else 0
        message.save()
        
        return render(request, 'chat/feedback_buttons.html', {'message': message})
    return HttpResponse("No autorizado", status=403)


def fetch_model_response(prompt, model_name):
    start_time = time.time()
    token = os.environ.get('NVIDIA_API_KEY')
    endpoint = 'https://integrate.api.nvidia.com/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model_name,
        'messages': [{"role": "user", "content": prompt}],
        'max_tokens': 1024,
        'temperature': 0.7
    }
    
    try:
        # TIMEOUT AUMENTADO A 90 PARA DEEPSEEK
        res = requests.post(endpoint, headers=headers, json=payload, timeout=90)
        res.raise_for_status()
        content = res.json().get('choices')[0].get('message').get('content')
    except Exception as e:
        content = f"Error de conexión con {model_name}: {str(e)}"
        
    end_time = time.time()
    
    return {
        "name": model_name,
        "content": content,
        "time": round(end_time - start_time, 2)
    }

@login_required
def compare_models_view(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")
        
        model_1 = request.POST.get("model_1", "google/gemma-2-2b-it")
        model_2 = request.POST.get("model_2", "meta/llama-3.3-70b-instruct")
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(fetch_model_response, prompt, model_1)
            future2 = executor.submit(fetch_model_response, prompt, model_2)
            
            result1 = future1.result()
            result2 = future2.result()
            
        titulo_duelo = f"⚖️ Duelo: {prompt[:25]}..."
        nueva_conv = Conversation.objects.create(
            user=request.user, 
            title=titulo_duelo,
            ai_model=model_1 
        )
        
        Message.objects.create(conversation=nueva_conv, role='user', content=prompt)
        
        texto_ia1 = f"**[{result1['name']}]** (⏱️ {result1['time']}s)\n\n{result1['content']}"
        Message.objects.create(conversation=nueva_conv, role='assistant', content=texto_ia1)
        
        texto_ia2 = f"**[{result2['name']}]** (⏱️ {result2['time']}s)\n\n{result2['content']}"
        Message.objects.create(conversation=nueva_conv, role='assistant', content=texto_ia2)

        return render(request, "chat/compare_results.html", {
            "result1": result1,
            "result2": result2,
            "saved_conv_id": nueva_conv.id 
        })
        
    return render(request, "chat/compare.html")

@login_required
def generate_shared_link(request, conv_id):
    chat = get_object_or_404(Conversation, id=conv_id, user=request.user)
    
    SharedLink.objects.filter(conversation=chat, expires_at__lt=timezone.now()).delete()
    shared_link = SharedLink.objects.create(conversation=chat)
    link_url = request.build_absolute_uri(reverse('shared_chat_view', args=[shared_link.id]))
    
    return render(request, 'chat/share_link.html', {
        'link_url': link_url,
        'chat': chat,
        'expires_at': shared_link.expires_at
    })

@login_required
def shared_chat_view(request, link_id):
    shared_link = get_object_or_404(SharedLink, id=link_id)
    
    if not shared_link.is_valid():
        return HttpResponse("Este enlace ha caducado o ya no es válido.", status=410)
        
    chat = shared_link.conversation
    messages = chat.messages.all().order_by('created_at')
    
    return render(request, 'chat/shared_chat.html', {
        'conversation': chat, 
        'messages': messages,
        'owner': chat.user
    })