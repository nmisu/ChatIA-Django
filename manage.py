#!/usr/bin/env python
"""
Script principal de arranque y gestión para el entorno del proyecto.
Encargado de canalizar las instrucciones por la terminal de Django.
"""
import os as os_module
import sys as system_module

def execute_administrative_tasks():
    """Inicializa la configuración y procesa los comandos."""
    
    # Vinculamos las variables de entorno a la carpeta config
    os_module.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    
    try:
        from django.core.management import execute_from_command_line as launch_django_cmd
    except ImportError as fatal_error:
        raise ImportError(
            "Fallo crítico: No se ha detectado la instalación de Django. "
            "Asegúrate de que el framework está instalado y de que has "
            "activado el entorno virtual correcto antes de continuar."
        ) from fatal_error
        
    # Pasamos los parámetros de la consola al núcleo de la aplicación
    launch_django_cmd(system_module.argv)

if __name__ == "__main__":
    execute_administrative_tasks()
