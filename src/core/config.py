import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv('ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    API_URL = os.getenv('API_URL', 'https://api.example.com')

    # Akamai Configuration
    AKAMAI_API_URL = os.getenv('AKAMAI_API_URL')
    AKAMAI_API_TOKEN = os.getenv('AKAMAI_API_TOKEN')

    # Database Configuration
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    # Email Configuration
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

    # Google Drive Configuration
    GOOGLE_DRIVE_FOLDER = os.getenv('GOOGLE_DRIVE_FOLDER')
    GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv('GOOGLE_DRIVE_CREDENTIALS_PATH')

config = Config()
