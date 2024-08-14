import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from src.core.config import config
from src.core.logger import logger

def send_email(to_address, pdf):
    logger.info(f"Enviando e-mail para {to_address}...")
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL_USER
    msg['To'] = to_address
    msg['Subject'] = "Proteção Web - Relatório Semanal"

    with open('templates/email_template.html') as file:
        html = file.read()

    msg.attach(MIMEText(html, 'html'))

    with open(pdf, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename="relatorio_semanal.pdf")
        msg.attach(attachment)

    with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as server:
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    logger.info(f"E-mail enviado com sucesso para {to_address}.")
