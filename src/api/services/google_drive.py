"""
Serviço para integração com Google Drive (autenticação, criação de pastas e upload de PDFs).
"""

import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.core.config import config
from src.core.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """
    Autentica no Google Drive usando conta de serviço.
    """
    creds_path = config.GOOGLE_DRIVE_CREDENTIALS_PATH
    if not os.path.exists(creds_path):
        logger.error(f"Credenciais do Google Drive não encontradas: {creds_path}")
        raise FileNotFoundError("Credenciais do Google Drive não encontradas.")

    try:
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        logger.info("Autenticado com sucesso no Google Drive.")
        return service
    except Exception as e:
        logger.error(f"Erro ao autenticar no Google Drive: {e}")
        raise

def upload_to_google_drive(service, file_path, folder_id):
    """
    Faz o upload de um arquivo para o Google Drive na pasta especificada.

    Args:
        service: Instância autenticada do Google Drive (googleapiclient.discovery.Resource).
        file_path (str): Caminho para o arquivo a ser enviado.
        folder_id (str): ID da pasta no Google Drive onde o arquivo será armazenado.

    Returns:
        str: ID do arquivo enviado.
    """
    if not os.path.exists(file_path):
        logger.error(f"Arquivo não encontrado para upload: {file_path}")
        raise ValueError(f"Arquivo não encontrado: {file_path}")

    if not folder_id:
        logger.error("ID da pasta no Google Drive não foi fornecido.")
        raise ValueError("folder_id é obrigatório para upload.")

    try:
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        logger.info(f"Arquivo '{file_path}' enviado com sucesso ao Google Drive.")
        return file.get('id')
    except Exception as e:
        logger.error(f"Erro ao fazer upload do arquivo '{file_path}': {e}")
        raise

def create_folder_if_not_exists(service, folder_name, parent_folder_id=None):
    """
    Cria uma pasta no Google Drive se ela não existir.

    Args:
        service: Instância autenticada do Google Drive.
        folder_name (str): Nome da pasta a ser criada.
        parent_folder_id (str, optional): ID da pasta pai.

    Returns:
        str: ID da pasta criada/existente.
    """
    try:
        query = (
            f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        )
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        items = results.get('files', [])

        if not items:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]

            folder = service.files().create(body=file_metadata, fields='id').execute()
            logger.info(f"Pasta '{folder_name}' criada com sucesso no Google Drive.")
            return folder.get('id')
        else:
            folder_id = items[0].get('id')
            logger.info(f"Pasta '{folder_name}' já existe no Google Drive. ID: {folder_id}")
            return folder_id
    except Exception as e:
        logger.error(f"Erro ao criar/verificar pasta '{folder_name}': {e}")
        raise

def store_pdf_in_drive(company_name, file_path):
    """
    Armazena um PDF no Google Drive em uma estrutura de pastas organizada por data e empresa.

    Estrutura padrão:
      - backup_relatorio_semanal_algar (pasta raiz)
        - {company_name} (subpasta)
          - relatorio_semanal_{DD-MM-YYYY} (subpasta)
            - {pdf_file}.pdf

    Args:
        company_name (str): Nome da empresa (subpasta).
        file_path (str): Caminho do arquivo PDF a ser armazenado.
    """
    try:
        service = authenticate_google_drive()
        today = datetime.date.today()

        # Pasta raiz
        parent_folder_id = create_folder_if_not_exists(service, config.GOOGLE_DRIVE_FOLDER)

        # Pasta da empresa
        company_folder_id = create_folder_if_not_exists(service, company_name, parent_folder_id)

        # Pasta da data
        report_folder_name = f"relatorio_semanal_{today.strftime('%d-%m-%Y')}"
        report_folder_id = create_folder_if_not_exists(service, report_folder_name, company_folder_id)

        upload_to_google_drive(service, file_path, report_folder_id)
        logger.info(f"PDF '{file_path}' armazenado com sucesso no Google Drive.")
    except Exception as e:
        logger.error(f"Erro ao armazenar PDF no Google Drive: {e}")
        raise
