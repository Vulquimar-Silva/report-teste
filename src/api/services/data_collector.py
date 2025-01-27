import requests
from src.core.config import config
from src.core.logger import logger

def collect_data():
    """
    Coleta dados do endpoint configurado (fake ou Akamai).
    """
    logger.info("Iniciando coleta de dados do endpoint configurado...")

    api_env = config.API_TYPE  # 'fake' ou 'akamai'
    if api_env not in ["fake", "akamai"]:
        logger.error(f"Ambiente de API inválido: {api_env}.")
        raise ValueError(f"Ambiente de API inválido: {api_env}")

    # Montar URL final. Se for 'fake', talvez colocar /data no final, se não estiver no .env
    url = config.API_ENDPOINT
    if api_env == "fake" and not url.endswith("/data"):
        url += "/data"

    headers = {}
    if api_env == "akamai":
        headers = {
            'Authorization': f"Bearer {config.AKAMAI_API_TOKEN}",
            'Content-Type': 'application/json'
        }

    logger.debug(f"URL configurada: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        response_data = response.json()
        if not response_data:
            logger.warning(f"A resposta da API ({api_env}) está vazia ou inválida.")
            return {}

        logger.info(f"Dados coletados com sucesso do ambiente '{api_env}'.")
        return response_data

    except requests.RequestException as e:
        logger.error(f"Erro ao acessar a API '{api_env}' no endpoint '{url}': {e}")
        raise
