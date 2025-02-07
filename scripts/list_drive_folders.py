from googleapiclient.discovery import build
from google.oauth2 import service_account
from src.core.config import config
from src.core.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """Autentica no Google Drive usando Service Account."""
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_DRIVE_CREDENTIALS_PATH, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

def get_file_path(service, file_id):
    """Retorna o caminho completo do arquivo no Google Drive."""
    try:
        file = service.files().get(fileId=file_id, fields='id, name, parents').execute()
        path = []
        
        # Percorre a árvore de pastas até a raiz
        while 'parents' in file:
            parent_id = file['parents'][0]
            parent = service.files().get(fileId=parent_id, fields='id, name, parents').execute()
            path.append(parent['name'])
            file = parent

        return " / ".join(reversed(path))

    except Exception as e:
        logger.error(f"Erro ao obter caminho do arquivo: {e}")
        return "Erro ao obter caminho"

def list_drive_structure():
    """Lista a estrutura completa das pastas e arquivos armazenados."""
    try:
        service = authenticate_google_drive()
        query = "mimeType!='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, spaces='drive', fields='files(id, name, parents)').execute()
        items = results.get('files', [])

        if not items:
            print("Nenhum arquivo encontrado.")
            return

        print("\n🔍 **Estrutura Completa do Google Drive:**\n")
        for item in items:
            path = get_file_path(service, item['id'])
            print(f"📄 Arquivo: {item['name']}\n📂 Caminho: {path}\n{'-'*50}")

    except Exception as e:
        logger.error(f"Erro ao listar estrutura do Google Drive: {e}")
        print(f"Erro ao listar estrutura: {e}")

if __name__ == "__main__":
    list_drive_structure()
