from googleapiclient.discovery import build
from google.oauth2 import service_account
from src.core.config import config
from src.core.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_DRIVE_CREDENTIALS_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def share_folder_with_email(folder_id, email):
    try:
        service = authenticate_google_drive()
        permission = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': email
        }
        service.permissions().create(
            fileId=folder_id,
            body=permission,
            fields='id'
        ).execute()
        logger.info(f"Pasta {folder_id} compartilhada com sucesso com {email}.")
    except Exception as e:
        logger.error(f"Erro ao compartilhar a pasta {folder_id}: {e}")
        raise

if __name__ == "__main__":
    # Substitua pelo ID da pasta e o e-mail pessoal
    folder_id = "1qKEKl80LswWtGMOW8pZD5Ol0RGlLlSuf"
    email = "vulquimarfdsj@gmail.com"
    share_folder_with_email(folder_id, email)
