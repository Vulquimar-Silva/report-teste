from jinja2 import Environment, FileSystemLoader
import pdfkit
from src.core.logger import logger
from src.api.services.google_drive import store_pdf_in_drive

env = Environment(loader=FileSystemLoader('templates'))

def generate_pdf(data):
    logger.info("Gerando PDF...")
    template = env.get_template('pdf_template.html')
    html_content = template.render(data)
    pdf_path = f"/tmp/{data['subscriberId']}_relatorio_semanal.pdf"
    pdfkit.from_string(html_content, pdf_path)
    logger.info("PDF gerado com sucesso.")
    store_pdf_in_drive(data['subscriberId'], pdf_path)
    return pdf_path
