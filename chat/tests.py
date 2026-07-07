from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Conversation, Message, Profile
import json

class ChatIATestCase(TestCase):
    def setUp(self):
        """
        Configuración inicial: se ejecuta ANTES de cada test.
        Creamos dos usuarios para probar escenarios de seguridad y cruce de datos.
        """
        self.client = Client()
        
        # Usuario principal
        self.user1 = User.objects.create_user(username='tester1', password='password123')
        self.profile1 = Profile.objects.create(user=self.user1, alias='Tester Uno', theme='oscuro')
        
        # Usuario malicioso/secundario
        self.user2 = User.objects.create_user(username='hacker2', password='password123')
        
        # Conversación del usuario 1
        self.conv1 = Conversation.objects.create(
            user=self.user1, 
            title="Chat de prueba",
            ai_model="google/gemma-2-2b-it"
        )
        
        # Mensajes en la conversación
        self.msg_user = Message.objects.create(
            conversation=self.conv1, 
            role='user', 
            content="Hola IA"
        )
        self.msg_ia = Message.objects.create(
            conversation=self.conv1, 
            role='assistant', 
            content="¡Hola! ¿En qué puedo ayudarte?",
            feedback=0
        )

    # ---------------------------------------------------------
    # 1. TESTS UNITARIOS PARA MODELOS
    # ---------------------------------------------------------
    def test_model_conversation_creation(self):
        """Prueba que los modelos guardan correctamente los valores por defecto"""
        self.assertEqual(self.conv1.title, "Chat de prueba")
        self.assertEqual(self.conv1.user.username, 'tester1')
        self.assertEqual(self.conv1.ai_model, "google/gemma-2-2b-it") # Verificamos el selector de modelo

    def test_model_message_feedback_default(self):
        """Prueba que los mensajes del asistente nacen con feedback neutro (0)"""
        self.assertEqual(self.msg_ia.feedback, 0)
        self.assertEqual(self.msg_ia.role, 'assistant')

    # ---------------------------------------------------------
    # 2. CONDICIONES DE ERROR Y SEGURIDAD
    # ---------------------------------------------------------
    def test_error_access_other_user_chat(self):
        """Prueba que un usuario no puede entrar en la conversación de otro"""
        # Hacemos login con el usuario 2
        self.client.login(username='hacker2', password='password123')
        
        # Intentamos acceder al detalle del chat del usuario 1
        url = reverse('conversation_detail', args=[self.conv1.id])
        response = self.client.get(url)
        
        # Debe devolver un error 404 (Not Found) porque el get_object_or_404 filtra por usuario
        self.assertEqual(response.status_code, 404)

    def test_error_rate_other_user_message(self):
        """Prueba que un usuario no puede votar (Like/Dislike) en mensajes ajenos"""
        self.client.login(username='hacker2', password='password123')
        
        url = reverse('rate_message', args=[self.msg_ia.id, 'like'])
        response = self.client.post(url)
        
        # Nuestro views.py devuelve 403 Forbidden si el usuario no coincide
        self.assertEqual(response.status_code, 403)

    # ---------------------------------------------------------
    # 3. LLAMADAS CONSECUTIVAS Y APIs INTERNAS
    # ---------------------------------------------------------
    def test_internal_api_export_json(self):
        """Prueba la API interna de exportar conversación a JSON"""
        self.client.login(username='tester1', password='password123')
        
        url = reverse('export_conversation_json', args=[self.conv1.id])
        response = self.client.get(url)
        
        # Verificamos que la llamada es exitosa
        self.assertEqual(response.status_code, 200)
        
        # Verificamos que el contenido es un JSON válido y tiene la estructura correcta
        data = json.loads(response.content)
        self.assertEqual(data['titulo'], "Chat de prueba")
        self.assertEqual(data['usuario'], "tester1")
        self.assertEqual(len(data['mensajes']), 2) # Debe haber 2 mensajes (usuario e IA)

    def test_consecutive_calls_rate_message_toggle(self):
        """Prueba el escenario de llamadas consecutivas (Toggle de Like/Dislike)"""
        self.client.login(username='tester1', password='password123')
        url_like = reverse('rate_message', args=[self.msg_ia.id, 'like'])
        
        # 1ª Llamada: Le da Like
        self.client.post(url_like)
        self.msg_ia.refresh_from_db() # Refrescamos el objeto desde la BD
        self.assertEqual(self.msg_ia.feedback, 1)
        
        # 2ª Llamada consecutiva: Le vuelve a dar Like (debe anularse y volver a 0)
        self.client.post(url_like)
        self.msg_ia.refresh_from_db()
        self.assertEqual(self.msg_ia.feedback, 0)