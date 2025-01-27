"""
Serviço para envio de e-mails com um anexo em PDF.
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from src.core.config import config
from src.core.logger import logger

def send_email(to_addresses, pdf_path, subject="Proteção Web - Relatório Semanal", email_body=None):
    """
    Envia um e-mail com um anexo em PDF.

    Args:
        to_addresses (list): Lista de endereços de e-mail para envio.
        pdf_path (str): Caminho para o arquivo PDF a ser anexado.
        subject (str): Assunto do e-mail.
        email_body (str): Corpo do e-mail em HTML ou texto plano.
    """
    logger.info(f"Preparando e-mail para {to_addresses}...")

    # Verifica se o arquivo PDF existe
    if not os.path.exists(pdf_path):
        logger.error(f"Arquivo PDF não encontrado: {pdf_path}")
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_path}")

    # Monta a mensagem
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL_USER
    msg['To'] = ', '.join(to_addresses)
    msg['Subject'] = subject

    # Verifica se há email_body ou template
    email_template_path = 'templates/email_template.html'
    if email_body:
        msg.attach(MIMEText(email_body, 'html'))
        logger.info("Usando o corpo do e-mail fornecido (HTML) dinamicamente.")
    elif os.path.exists(email_template_path):
        # Carrega o template HTML padrão
        with open(email_template_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        msg.attach(MIMEText(html_content, 'html'))
        logger.info("Template HTML carregado com sucesso.")
    else:
        # Fallback: texto simples
        logger.warning("Template HTML não encontrado. Usando corpo de e-mail padrão em texto.")
        msg.attach(MIMEText("Segue em anexo o relatório solicitado.", 'plain'))

    # Anexa o PDF
    try:
        with open(pdf_path, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype="pdf")
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(pdf_path))
            msg.attach(attachment)
        logger.info(f"Anexo PDF adicionado: {os.path.basename(pdf_path)}")
    except Exception as e:
        logger.error(f"Erro ao anexar o arquivo PDF: {e}")
        raise

    # Envia o e-mail via SMTP (TLS)
    try:
        with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            server.sendmail(msg['From'], to_addresses, msg.as_string())
        logger.info(f"E-mail enviado com sucesso para {to_addresses}.")
    except smtplib.SMTPAuthenticationError:
        logger.critical("Falha na autenticação SMTP. Verifique as credenciais.")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        raise
