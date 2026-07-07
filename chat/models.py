import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Es mejor práctica obtener el modelo de usuario de esta forma
UserAccount = get_user_model()

class Conversation(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='chats')
    title = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    MODEL_CHOICES = [
        ('google/gemma-2-2b-it', 'Gemma 2 (2B) - Ultra rápido'),
        ('meta/llama-3.1-8b-instruct', 'Llama 3.1 (8B) - Equilibrado y estable'),
        ('deepseek-ai/deepseek-v4-flash', 'DeepSeek V4 Flash - Optimizado y rápido'),
        ('deepseek-ai/deepseek-v4-pro', 'DeepSeek V4 Pro - Razonamiento profundo'),
    ]    
    
    ai_model = models.CharField(
        max_length=100, 
        choices=MODEL_CHOICES, 
        default='google/gemma-2-2b-it' 
    )

    def __str__(self):
         return f"Chat: {self.title}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.IntegerField(default=0) # 0: sin voto, 1: Like, -1: Dislike

    def __str__(self):
        return f"[{self.role}] - {self.content[:40]}..."

class Profile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='profile')
    alias = models.CharField(max_length=60, null=True, blank=True)
    theme = models.CharField(max_length=30, default="rosa")

    def __str__(self):
        return f"Perfil de {self.user.username}"

def default_expiration():
    # El enlace caducará automáticamente en 24 horas
    return timezone.now() + timedelta(days=1)

class SharedLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='shared_links')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiration)

    def is_valid(self):
        return timezone.now() < self.expires_at