"""
Configuración de enrutamiento principal.
"""
from django.contrib import admin
from django.urls import path, include
import django.contrib.auth.views as authentication_views

urlpatterns = [
    # Panel de administración
    path("admin/", admin.site.urls),

    # Gestión de accesos
    path(
        'login/', 
        authentication_views.LoginView.as_view(template_name='chat/login.html'), 
        name='login'
    ),
    path(
        'logout/', 
        authentication_views.LogoutView.as_view(), 
        name='logout'
    ),

    # Inclusión de las rutas de la aplicación
    path('', include('chat.urls')),
]