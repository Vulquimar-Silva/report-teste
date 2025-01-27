"""
Endpoint responsável por expor dados vindos da API configurada (Akamai ou Fake).
"""

from flask import Blueprint, jsonify
import requests
from src.core.security import token_required
from src.core.config import config
from src.core.logger import logger

akamai_bp = Blueprint('akamai', __name__)

@akamai_bp.route('/akamai/data', methods=['GET'])
@token_required
def get_akamai_data(current_user):
    """
    Endpoint para coletar dados da API configurada (Akamai ou Fake).

    - Verifica qual tipo de API está sendo usada (config.API_TYPE).
    - Monta a URL de acordo com config.API_ENDPOINT ou config.AKAMAI_API_URL.
    - Faz a requisição HTTP e retorna o JSON.
    """
    logger.info(f"Usuário '{current_user}' iniciou requisição para a API configurada.")

    # Escolhe o endpoint com base no tipo de API
    if config.API_TYPE == 'fake':
        # Pode ser ou FAKE_API_URL ou API_ENDPOINT
        api_url = config.API_ENDPOINT  # se config.API_ENDPOINT já aponta para /data
    else:
        api_url = f"{config.AKAMAI_API_URL}/endpoint"

    logger.info(f"Endpoint configurado: {api_url}")

    try:
        headers = {}
        if config.API_TYPE != 'fake':
            headers = {
                'Authorization': f"Bearer {config.AKAMAI_API_TOKEN}",
                'Content-Type': 'application/json'
            }

        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            logger.info("Dados da API configurada coletados com sucesso.")
            return jsonify(response.json()), 200
        elif response.status_code == 401:
            logger.warning("API retornou 'Unauthorized'. Verifique o token de autenticação.")
            return jsonify({
                'error': 'Unauthorized access to API. Check your token.',
                'status_code': response.status_code
            }), 401
        else:
            logger.error(f"Erro ao acessar a API configurada: {response.status_code} - {response.text}")
            return jsonify({
                'error': 'Failed to retrieve data from API',
                'status_code': response.status_code,
                'details': response.text
            }), response.status_code

    except requests.Timeout:
        logger.error("A requisição para a API configurada expirou (timeout). Verifique rede ou endpoint.")
        return jsonify({
            'error': 'Request to API timed out',
            'details': 'Connection timed out. Please check your network or the API endpoint.'
        }), 504
    except requests.RequestException as e:
        logger.error(f"Erro de conexão com a API configurada: {str(e)}")
        return jsonify({
            'error': 'An error occurred while connecting to the API',
            'details': str(e)
        }), 500
