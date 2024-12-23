# Regala y Recibe

**Regala y Recibe** es una aplicación web desarrollada en **Django** que permite a los usuarios participar en un sistema de donaciones e intercambios de objetos. Este proyecto es parte del trabajo final para la obtención del título de **Programación y Análisis de Sistemas**.

## Descripción
La aplicación tiene como objetivo promover el intercambio y donación de bienes entre los usuarios de una comunidad. Los participantes pueden:

- Publicar objetos que desean donar.
- Proponer intercambios de bienes con otros usuarios.
- Administrar propuestas enviadas y recibidas.
- Gestionar notificaciones sobre donaciones e intercambios aceptados o rechazados.

### Características principales
- **Sistema de donaciones:** Los usuarios pueden publicar objetos para regalar y gestionar solicitudes de otros usuarios interesados.
- **Sistema de intercambio:** Los usuarios pueden proponer intercambiar objetos, completando un flujo interactivo para aceptar o rechazar propuestas.
- **Notificaciones:** Se notifica a los usuarios cuando se reciben propuestas y cuando estas son aceptadas o rechazadas.
- **Gestión visual:** Un "carrito" organiza todas las propuestas activas de donaciones e intercambios, ofreciendo un diseño estilizado y fácil de usar.

## Tecnologías utilizadas
El proyecto fue desarrollado con las siguientes herramientas y tecnologías:

- **Lenguaje principal:** Python
- **Framework backend:** Django
- **Base de datos:** SQLite (configurable para otros motores como PostgreSQL o MySQL)
- **Frontend:** HTML, CSS y Bootstrap para el diseño responsivo
- **Control de versiones:** Git y GitHub

## Instalación y configuración
Sigue los pasos a continuación para configurar el proyecto localmente:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/GeorgeAbou/Regala-Y-Recibe_APP_Django.git
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   - Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
     ```env
     SECRET_KEY=tu_clave_secreta
     DEBUG=True
     DATABASE_NAME=db.sqlite3
     ```

5. **Realiza las migraciones de la base de datos:**
   ```bash
   python manage.py migrate
   ```

6. **Inicia el servidor local:**
   ```bash
   python manage.py runserver
   ```

7. Accede a la aplicación en tu navegador: `http://127.0.0.1:8000`

## Uso
1. Regístrate como usuario para acceder a las funcionalidades de la plataforma.
2. Publica objetos para donar o postúlate para recibir donaciones.
3. Gestiona propuestas de intercambio.
4. Visualiza el historial de transacciones completadas.

## Contribuciones
Este proyecto es parte del trabajo final de título y actualmente no admite contribuciones externas. Sin embargo, cualquier sugerencia o comentario será bienvenido. Puedes abrir un **issue** en el repositorio o contactarme directamente.

## Autor
- **George Karin Abuchanab**
- Estudiante de **Programación y Análisis de Sistemas**



