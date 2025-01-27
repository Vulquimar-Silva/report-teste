import os
import tempfile
import pdfkit
from jinja2 import Environment, FileSystemLoader, TemplateError, TemplateNotFound
from src.core.logger import logger
from src.api.services.google_drive import store_pdf_in_drive

# Diretório onde ficam os templates
TEMPLATE_DIR = os.getenv('TEMPLATE_DIR', 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_pdf(data):
    """
    Gera um PDF com base em 'pdf_template.html' e armazena no Google Drive
    com um nome de arquivo mais profissional e descritivo.
    """
    logger.info("Iniciando a geração do PDF...")

    # Carrega o template
    try:
        template = env.get_template('pdf_template.html')
    except (TemplateNotFound, TemplateError) as e:
        logger.error(f"Erro ao carregar o template 'pdf_template.html': {e}")
        raise

    # Renderiza o HTML com os dados fornecidos
    try:
        html_content = template.render(data)
        logger.info("Template renderizado com sucesso.")
    except TemplateError as e:
        logger.error(f"Erro ao renderizar o template do PDF: {e}")
        raise

    # Exemplo de obtenção de campos para montar um nome profissional
    subscriber_id = data.get('subscriberId', 'desconhecido')
    company_name = data.get('company_name', 'MinhaEmpresa')
    period = data.get('period', '0000-00-00')
    
    # Substitui espaços por underscores ou retira caracteres especiais, se preferir
    safe_company = company_name.replace(' ', '_')
    safe_period = period.replace('/', '-').replace(' ', '_')

    # Gera um nome de arquivo, por exemplo: Relatorio_MinhaEmpresa_12345_27-01-2025.pdf
    pdf_filename = f"Relatorio_{safe_company}_{subscriber_id}_{safe_period}.pdf"

    # Cria caminho temporário
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, pdf_filename)

    # Opções do wkhtmltopdf (para habilitar acesso local)
    pdf_options = {
        "--enable-local-file-access": ""
    }

    try:
        pdfkit.from_string(html_content, pdf_path, options=pdf_options)
        logger.info(f"PDF gerado com sucesso: {pdf_path}")
    except OSError as e:
        logger.error(f"Erro ao gerar PDF via pdfkit: {e}")
        raise

    # Envia para Google Drive
    try:
        # store_pdf_in_drive() deve usar os metadados com 'name': os.path.basename(pdf_path)
        # para nomear corretamente no Drive
        store_pdf_in_drive(company_name, pdf_path)
        logger.info(f"PDF '{pdf_filename}' armazenado no Google Drive para {company_name}.")
    except Exception as e:
        logger.error(f"Erro ao armazenar PDF no Google Drive: {e}")
        raise
    finally:
        # Remove o arquivo local temporário
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.debug(f"Arquivo temporário {pdf_path} removido.")

    return pdf_path
