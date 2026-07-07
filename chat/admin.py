from django.contrib import admin
from . import models

# Registramos los modelos usando decoradores y mejoramos su visualización
@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at') # Muestra estas 3 columnas
    search_fields = ('title', 'user__username')    # Añade una barra de búsqueda

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'created_at')
    list_filter = ('role',)                        # Añade un filtro lateral por rol (user/assistant)

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'alias', 'theme')