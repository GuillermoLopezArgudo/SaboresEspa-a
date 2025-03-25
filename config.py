import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')
    MYSQL_USER = os.getenv('MYSQL_USER', 'user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '1234')
    MYSQL_DB = os.getenv('MYSQL_DB', 'RecetasEspañolas')