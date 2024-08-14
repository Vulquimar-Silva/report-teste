from apscheduler.schedulers.background import BackgroundScheduler
from src.api.services.data_collector import DataCollector
from src.api.services.data_transformer import DataTransformer
from src.api.services.pdf_generator import generate_pdf
from src.api.services.email_sender import send_email
from src.core.logger import logger
import os

scheduler = BackgroundScheduler()

def schedule_tasks():
    # Coleta e transforma os dados diariamente
    scheduler.add_job(run_etl_job, 'interval', days=1, hour=2, minute=0)
    # Envia os relatórios nas terças, quintas e sábados
    scheduler.add_job(send_reports, 'cron', day_of_week='tue,thu,sat', hour=3, minute=0)
    scheduler.start()

def run_etl_job():
    try:
        data_collector = DataCollector()
        raw_data = data_collector.collect_dns_data()

        data_transformer = DataTransformer(os.getenv('DATABASE_URL'))
        transformed_data = data_transformer.transform_and_load(raw_data)

        logger.info("ETL job completed successfully.")
        return transformed_data
    except Exception as e:
        logger.error(f"ETL job failed: {e}")
        # Notificar falha (e.g., enviar e-mail, Slack, etc.)
        return None

def send_reports():
    transformed_data = run_etl_job()
    if transformed_data:
        for client_data in transformed_data:
            try:
                pdf = generate_pdf(client_data)
                send_email(client_data['email'], pdf)
                logger.info(f"Report sent successfully to {client_data['email']}.")
            except Exception as e:
                logger.error(f"Failed to send report to {client_data['email']}: {e}")
                # Notificar falha (e.g., enviar e-mail, Slack, etc.)
    else:
        logger.error("No data available for report generation.")

schedule_tasks()
