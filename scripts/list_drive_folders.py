import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from src.core.config import config
from src.core.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate_google_drive():
    """Autentica com o Google Drive usando uma conta de serviço."""
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_DRIVE_CREDENTIALS_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def list_folders(service):
    """Lista todas as pastas criadas pela conta de serviço."""
    try:
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name, parents)',
            orderBy='createdTime desc'
        ).execute()
        folders = results.get('files', [])
        if not folders:
            print("Nenhuma pasta encontrada.")
            return
        print("Pastas encontradas:")
        for folder in folders:
            print(f"Nome: {folder['name']} | ID: {folder['id']} | Pais: {folder.get('parents', 'Nenhum')}")
    except Exception as e:
        logger.error(f"Erro ao listar pastas: {e}")
        raise

if __name__ == "__main__":
    service = authenticate_google_drive()
    list_folders(service)
