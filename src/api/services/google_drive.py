import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.core.config import config

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Autentica com o Google Drive usando uma conta de serviço."""
    creds = service_account.Credentials.from_service_account_file(
        config.GOOGLE_DRIVE_CREDENTIALS_PATH, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_to_google_drive(file_path, folder_id):
    service = authenticate_google_drive()
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
    return file.get('id')

def create_folder_if_not_exists(service, folder_name, parent_folder_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
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
        return folder.get('id')
    else:
        return items[0].get('id')

def store_pdf_in_drive(company_name, file_path):
    service = authenticate_google_drive()
    today = datetime.date.today()
    folder_name = f"backup_relatorio_semanal_algar/{company_name}/relatorio_semanal_{today.strftime('%d-%m-%Y')}"
    parent_folder_id = create_folder_if_not_exists(service, 'backup_relatorio_semanal_algar')
    company_folder_id = create_folder_if_not_exists(service, company_name, parent_folder_id)
    report_folder_id = create_folder_if_not_exists(service, f"relatorio_semanal_{today.strftime('%d-%m-%Y')}", company_folder_id)
    upload_to_google_drive(file_path, report_folder_id)
