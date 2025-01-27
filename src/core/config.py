import os
from dotenv import load_dotenv
from src.core.logger import logger

load_dotenv()

class Config:
    """Carrega e valida as configurações do ambiente."""

    def __init__(self):
        self._validate_env()

        # Config Geral
        self.ENV = os.getenv('ENV', 'development')
        self.DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1']
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
        
        # API Geral
        self.API_URL = os.getenv('API_URL', 'https://api.example.com')
        self.API_TYPE = os.getenv('API_TYPE', 'fake').lower()  # 'fake' ou 'akamai'

        # Ajuste do endpoint, dependendo do tipo de API
        if self.API_TYPE == 'fake':
            # Agora PEGAMOS a URL exata do .env sem adicionar '/data' automaticamente.
            # Se você quiser '/data', coloque já no .env (FAKE_API_URL=http://host.docker.internal:3000/data).
            self.API_ENDPOINT = os.getenv('FAKE_API_URL', 'http://localhost:3000')
        elif self.API_TYPE == 'akamai':
            self.API_ENDPOINT = f"{os.getenv('AKAMAI_API_URL')}/endpoint"
        else:
            raise ValueError(f"API_TYPE inválido: {self.API_TYPE} (use 'fake' ou 'akamai')")

        self.AKAMAI_API_URL = os.getenv('AKAMAI_API_URL')
        self.AKAMAI_API_TOKEN = os.getenv('AKAMAI_API_TOKEN')

        # Database
        self.POSTGRES_USER = os.getenv('POSTGRES_USER')
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        self.POSTGRES_DB = os.getenv('POSTGRES_DB')
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
        self.DATABASE_URL = (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

        # E-mail
        self.EMAIL_HOST = os.getenv('EMAIL_HOST')
        self.EMAIL_PORT = self._safe_int(os.getenv('EMAIL_PORT'), 587)
        self.EMAIL_USER = os.getenv('EMAIL_USER')
        self.EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

        # Google Drive
        self.GOOGLE_DRIVE_FOLDER = os.getenv('GOOGLE_DRIVE_FOLDER')
        self.GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv('GOOGLE_DRIVE_CREDENTIALS_PATH')

        # Outras configs
        self.REQUIRES_AUTH = os.getenv('REQUIRES_AUTH', 'False').lower() == 'true'  # Exemplo

    def _safe_int(self, value, default):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def _validate_env(self):
        """Valida a existência das variáveis de ambiente obrigatórias."""
        required_vars = [
            'POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB',
            'POSTGRES_HOST', 'EMAIL_HOST', 'EMAIL_USER',
            'EMAIL_PASSWORD', 'GOOGLE_DRIVE_CREDENTIALS_PATH'
        ]

        if os.getenv('API_TYPE', 'fake').lower() == 'akamai':
            required_vars.extend(['AKAMAI_API_URL', 'AKAMAI_API_TOKEN'])
        else:  # se 'fake'
            required_vars.append('FAKE_API_URL')

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            missing = ", ".join(missing_vars)
            raise EnvironmentError(
                f"As seguintes variáveis obrigatórias estão ausentes no .env: {missing}"
            )
        else:
            logger.debug("Todas as variáveis de ambiente obrigatórias estão definidas.")


config = Config()
