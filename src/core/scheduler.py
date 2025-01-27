from apscheduler.schedulers.background import BackgroundScheduler
from src.api.services.data_collector import collect_data
from src.api.services.data_transformer import DataTransformer
from src.api.services.pdf_generator import generate_pdf
from src.core.logger import logger
from src.core.config import config
import os

scheduler = BackgroundScheduler()

def schedule_tasks(app):
    """
    Configura e inicia as tarefas agendadas no scheduler.
    """
    try:
        # Exemplo: job de ETL diário
        scheduler.add_job(
            run_etl_job,
            'cron',
            hour=int(os.getenv('ETL_HOUR', 2)),
            minute=int(os.getenv('ETL_MINUTE', 0)),
            args=[app],
            id='etl_job',
            replace_existing=True
        )

        scheduler.start()
        logger.info("Scheduler iniciado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao configurar o scheduler: {e}")
        raise

def run_etl_job(app):
    """
    Executa o processo ETL (coleta de dados + transformação + carga no banco).
    Retorna uma tupla (aggregated_data, df_raw).
    """
    logger.info("Executando job de ETL...")
    try:
        with app.app_context():
            raw_data = collect_data()
            data_transformer = DataTransformer(api_type=config.API_TYPE)
            aggregated_data, df_raw = data_transformer.transform_and_load(raw_data)

            logger.info("Job de ETL concluído com sucesso.")
            return (aggregated_data, df_raw)

    except Exception as e:
        logger.error(f"Erro durante o job de ETL: {e}")
        return None

def run_pdf_generation(app, etl_result):
    """
    Gera PDFs e armazena no Google Drive (sem envio de e-mail),
    usando a tupla (aggregated_data, df_raw) retornada pelo ETL.
    """
    logger.info("Gerando PDFs e armazenando no Google Drive (sem envio de e-mail)...")
    if etl_result is None:
        logger.warning("Nenhum dado para gerar PDFs (etl_result é None).")
        return

    aggregated_data, df_raw = etl_result

    # Se aggregator estiver vazio
    if hasattr(aggregated_data, 'empty') and aggregated_data.empty:
        logger.warning("DataFrame aggregator vazio, nenhum PDF será gerado.")
        return

    try:
        with app.app_context():
            # Exemplo: se todos os campos do template estiverem na 'df_raw'
            # Pega apenas a 1ª linha. Em produção, você poderia gerar 1 PDF por linha.
            # ou se preferir, itere sobre df_raw
            row0 = df_raw.iloc[0].to_dict()

            for _, agg_row in aggregated_data.iterrows():
                # Monta dicionário final para o PDF
                # Pegamos do aggregator: subscriberId, domain, requests, blocks
                # Pegamos do df_raw: company_name, period, e assim por diante
                pdf_data = {
                    "subscriberId": agg_row["subscriberId"],
                    "domain": agg_row["domain"],
                    "requests": agg_row["requests"],
                    "blocks": agg_row["blocks"],

                    "company_name": row0.get("company_name", "Empresa Padrão"),
                    "internet_id": row0.get("internet_id", "Conexão Desconhecida"),
                    "period": row0.get("period", "2025-01-01 a 2025-01-31"),

                    "threats_protection_count": row0.get("threats_protection_count", 0),
                    "malware_phishing_count": row0.get("malware_phishing_count", 0),
                    "web_filter_block_count": row0.get("web_filter_block_count", 0),
                    "botnet_count": row0.get("botnet_count", 0),

                    "akamai_total_requests": row0.get("akamai_total_requests", 0),
                    "akamai_threats_detected": row0.get("akamai_threats_detected", 0),
                    "akamai_safe_transactions": row0.get("akamai_safe_transactions", 0),

                    "malicious_site_1": row0.get("malicious_site_1", ""),
                    "malicious_attempts_1": row0.get("malicious_attempts_1", 0),
                    "malicious_site_2": row0.get("malicious_site_2", ""),
                    "malicious_attempts_2": row0.get("malicious_attempts_2", 0),
                    "malicious_site_3": row0.get("malicious_site_3", ""),
                    "malicious_attempts_3": row0.get("malicious_attempts_3", 0),
                    "malicious_site_4": row0.get("malicious_site_4", ""),
                    "malicious_attempts_4": row0.get("malicious_attempts_4", 0),

                    "most_accessed_sites": row0.get("most_accessed_sites", ""),
                    "transaction_site_1": row0.get("transaction_site_1", ""),
                    "transaction_count_1": row0.get("transaction_count_1", 0),
                    "transaction_site_2": row0.get("transaction_site_2", ""),
                    "transaction_count_2": row0.get("transaction_count_2", 0),
                    "transaction_site_3": row0.get("transaction_site_3", ""),
                    "transaction_count_3": row0.get("transaction_count_3", 0),
                    "transaction_site_4": row0.get("transaction_site_4", ""),
                    "transaction_count_4": row0.get("transaction_count_4", 0),
                    "transaction_site_5": row0.get("transaction_site_5", ""),
                    "transaction_count_5": row0.get("transaction_count_5", 0),
                    "total_transactions": row0.get("total_transactions", 0)
                }

                pdf_path = generate_pdf(pdf_data)
                logger.info(
                    f"PDF gerado e armazenado no Drive para subscriberId={agg_row['subscriberId']} domain={agg_row['domain']}."
                )

    except Exception as e:
        logger.error(f"Erro durante geração de PDFs: {e}")
