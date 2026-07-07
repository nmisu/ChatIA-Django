# Entrega convocatoria junio

CHAT IA - Proyecto Final 2025/2026

Aplicación web tipo chat asistente-IA desarrollada con Python, Django, HTML y Bootstrap.

## Datos
* Nombre: Amos-Nicolás Misu
* Titulación: Ing. Sistemas de Telecomunicacion
* Cuenta en laboratorios: nicolas
* Cuenta URJC: a.misu.2019@alumnos.urjc.es
* Vídeo (URL): https://youtu.be/rA003ufdkj0 (Parte obligatoria) / https://youtu.be/m0_IB1-M884 (Parte Opcional)
* Despliegue (URL): https://nmisu.pythonanywhere.com/
* Usuarios y contraseñas: holasoypepe/pepe12345 | daniel/dni20021 | usuariodeprueba1/1234usuario | usrprueba/12usuario
* Cuenta Admin Site: admin/admin1234

## Recursos y métodos HTTP
* Recurso: `/` (Landing page) | Métodos: GET
* Recurso: `/registro/` (Registro de usuarios) | Métodos: GET, POST
* Recurso: `/login/` (Inicio de sesión) | Métodos: GET, POST
* Recurso: `/logout/` (Cierre de sesión) | Métodos: POST
* Recurso: `/chats/` (Panel principal y buscador) | Métodos: GET
* Recurso: `/new/` (Crear conversación) | Métodos: GET, POST
* Recurso: `/c/<conversation_id>/` (Vista de chat y envío de mensajes) | Métodos: GET, POST
* Recurso: `/edit/<conversation_id>/` (Renombrar) | Métodos: GET, POST
* Recurso: `/drop/<conversation_id>/` (Eliminar chat) | Métodos: GET, POST
* Recurso: `/me/` (Perfil de usuario) | Métodos: GET, POST
* Recurso: `/info/` (Página de ayuda) | Métodos: GET
* Recurso: `/admin/` (Panel de administración Django) | Métodos: GET, POST

**Nuevos recursos (Funcionalidades Avanzadas):**
* Recurso: `/c/<conversation_id>/json/` (Exportación a JSON) | Métodos: GET
* Recurso: `/c/<conversation_id>/share/` (Generar enlace temporal) | Métodos: GET
* Recurso: `/share/<link_id>/` (Ver chat compartido) | Métodos: GET
* Recurso: `/rate/<message_id>/<action>/` (Feedback de mensajes) | Métodos: GET, POST
* Recurso: `/compare/` (Duelo de modelos LLM) | Métodos: GET, POST
* Recurso: `/pin/<conversation_id>/` (Fijar chat) | Métodos: GET, POST
* Recurso: `/archive/<conversation_id>/` (Archivar chat) | Métodos: GET, POST

## Resumen parte obligatoria
La práctica consiste en una aplicación web en la que se puede mantener una conversación con una IA, desarrollada con el framework Django y base de datos SQLite3.

La aplicación permite a cada usuario registrado y autenticado crear conversaciones, enviar prompts a un modelo LLM real (mediante la API de NVIDIA NIM) y recibir respuestas asíncronas.

**Características principales implementadas:**
* Admin Site para administrar los modelos de la base de datos.
* Sistema de registro y autenticación de usuarios.
* Historial persistente de conversaciones asociadas a cada usuario.
* Gestión completa del CRUD de conversaciones (crear, leer, renombrar y borrar).
* Gestión del perfil de usuario (alias personalizado y tema visual).
* Medidas de seguridad y UX (confirmación antes de borrar una conversación).
* Navegación fluida entre páginas principales (home, chat, perfil y ayuda).
* Integración real con API LLM externa.
* Separación visual de mensajes (Usuario vs Asistente).
* Estructura modular basada en modelos relacionales (`Conversation`, `Message`, `Profile`).

## Lista partes opcionales (Funcionalidades Extra)
Se han implementado múltiples funcionalidades que amplían significativamente los requisitos básicos del proyecto:

1. **Soporte Multi-chat Avanzado:**
   * **Fijar y Archivar:** Los usuarios pueden marcar conversaciones con chinchetas (fijadas arriba) o mandarlas a un cajón de archivados para mantener la bandeja limpia.
   * **Motor de Búsqueda:** Buscador integrado que filtra dinámicamente las conversaciones comprobando coincidencias tanto en el título del chat como en el contenido de los mensajes.

2. **Exportación y Enlaces Temporales:**
   * **Exportación JSON:** Funcionalidad para descargar el historial completo de una conversación en formato estructurado JSON.
   * **Compartir de forma segura:** Generación de enlaces únicos (UUID) y temporales (caducan a las 24h) que permiten a otros usuarios de la plataforma leer la conversación en un entorno de solo lectura.

3. **Duelo de IAs (Comparación de Modelos):**
   * Vista especial que permite lanzar un mismo *prompt* simultáneamente a dos modelos de IA distintos (ej. Llama 3.1 vs Gemma 2).
   * Sistema de peticiones concurrentes (`ThreadPoolExecutor`) que cronometra y muestra el tiempo de respuesta y el texto generado por cada modelo lado a lado.

4. **Selección Dinámica de Modelos por Chat:**
   * El usuario puede elegir y cambiar el modelo de IA (Gemma, Llama, Mistral) específico para cada conversación desde un menú desplegable en la propia vista de chat.

5. **Feedback de Mensajes:**
   * Sistema de valoración (Like / Dislike) en los mensajes generados por la IA para evaluar la calidad de las respuestas.

6. **Mejoras UX/UI y Tecnológicas:**
   * Actualización parcial del chat mediante **HTMX**, evitando recargas completas de la página al enviar mensajes.
   * Interfaz moderna, *responsive* y estructurada mediante **Bootstrap 5**.
   * Scroll automático suave al último mensaje recibido.
