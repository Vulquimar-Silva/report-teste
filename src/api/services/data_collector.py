import requests
from src.core.config import config
from src.core.logger import logger

def collect_data():
    logger.info("Coletando dados da API do Akamai...")
    headers = {
        'Authorization': f"Bearer {config.AKAMAI_API_TOKEN}",
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{config.AKAMAI_API_URL}/endpoint", headers=headers)
    response.raise_for_status()
    logger.info("Dados coletados com sucesso da API do Akamai.")
    return response.json()
