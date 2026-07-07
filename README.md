# ChatIA-Django
# ChatIA - Asistente Conversacional Full-Stack

ChatIA es una aplicación web interactiva desarrollada en Python y Django que simula el comportamiento de un asistente conversacional avanzado. El sistema integra modelos de lenguaje de gran escala (LLM) a través de API y utiliza HTMX para ofrecer una experiencia de usuario fluida y en tiempo real sin necesidad de recargar la página.

## Características Principales

* **Integración de Inteligencia Artificial:** Conexión programática con la API de NVIDIA/OpenAI para la generación de respuestas dinámicas mediante transmisión asíncrona de datos (streaming).
* **Actualizaciones Asíncronas (HTMX):** Interfaz de usuario reactiva que gestiona el envío de prompts y la actualización del historial de chat en tiempo real, optimizando el rendimiento y minimizando la carga del servidor.
* **Autenticación y Gestión de Sesiones:** Sistema de control de acceso seguro y protección de rutas. El sistema garantiza la privacidad segmentando el acceso para que cada usuario interactúe exclusivamente con su propio historial de conversaciones.
* **Persistencia de Datos:** Arquitectura de base de datos relacional implementada sobre SQLite3 para el almacenamiento estructurado de perfiles de usuario, configuraciones personalizadas y el registro completo del historial de mensajes.
* **Diseño Responsivo:** Interfaz construida mediante el motor de plantillas de Django y el framework Bootstrap para garantizar una correcta adaptabilidad y visualización tanto en entornos de escritorio como en dispositivos móviles.

## Stack Tecnológico

* **Backend:** Python 3, Django
* **Frontend:** HTML5, CSS3, Bootstrap, HTMX
* **Base de Datos:** SQLite3
* **Integraciones:** API RESTful (librería requests / Server-Sent Events)

## Instalación y Despliegue Local

Para ejecutar este proyecto en un entorno de desarrollo local, siga las siguientes instrucciones:

1. Clone el repositorio en su máquina local:
   ```bash
   git clone [https://github.com/nmisu/ChatIA-Django.git](https://github.com/nmisu/ChatIA-Django.git)
2. Navegue al directorio raíz del proyecto  
  cd ChatIA-Django
3. Cree un entorno virtual e instale las dependencias requeridas. 
python -m venv venv
  source venv/bin/activate  # En sistemas Windows utilice: venv\Scripts\activate
  pip install -r requirements.txt
4. Configure las variables de entorno necesarias. Cree un archivo .env en la raíz del proyecto y añada su clave de API
NVIDIA_API_KEY=su_clave_aqui
5. Aplique las migraciones correspondientes a la base de datos e inicie el servidor de desarrollo
  python manage.py migrate
  python manage.py runserver
6. Acceda a la aplicación abriendo un navegador web en la siguiente dirección: http://127.0.0.1:8000/
