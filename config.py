import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')  # Render proveerá esta URL
    MYSQL_USER = os.getenv('MYSQL_USER', 'user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'RecetasEspanyolas')
    # Añade configuración para producción
    UPLOAD_FOLDER_IMAGES = '/app/static/images'
    UPLOAD_FOLDER_VIDEOS = '/app/static/videos'