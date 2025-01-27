from googleapiclient.discovery import build
from google.oauth2 import service_account
from src.core.config import config
from src.core.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    """Autentica com o Google Drive usando as credenciais de serviço."""
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_DRIVE_CREDENTIALS_PATH, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def list_drive_files():
    """Lista todos os arquivos no Google Drive."""
    try:
        service = authenticate_google_drive()
        results = service.files().list(pageSize=100, fields="files(id, name)").execute()
        files = results.get('files', [])
        return files
    except Exception as e:
        logger.error(f"Erro ao listar os arquivos do Google Drive: {e}")
        return []

def delete_drive_file(file_id):
    """Deleta um arquivo no Google Drive."""
    try:
        service = authenticate_google_drive()
        service.files().delete(fileId=file_id).execute()
        logger.info(f"Arquivo com ID {file_id} deletado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao deletar o arquivo com ID {file_id}: {e}")

if __name__ == "__main__":
    # Listar arquivos
    files = list_drive_files()
    if not files:
        print("Nenhum arquivo encontrado no Google Drive.")
    else:
        print("Arquivos encontrados:")
        for file in files:
            print(f"Nome: {file['name']} | ID: {file['id']}")
        
        # Confirmar exclusão
        delete_all = input("Deseja deletar todos os arquivos listados? (sim/não): ").strip().lower()
        if delete_all == "sim":
            for file in files:
                delete_drive_file(file['id'])
        else:
            file_id = input("Digite o ID do arquivo que deseja deletar: ").strip()
            delete_drive_file(file_id)
