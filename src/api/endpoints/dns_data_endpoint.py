"""
Endpoint responsável por coletar dados DNS de uma API externa (Akamai ou Fake).
"""

from flask import Blueprint, jsonify
from src.core.security import token_required
from src.api.services.data_collector import collect_data
from src.core.logger import logger
from src.core.config import config

dns_data_bp = Blueprint('dns_data', __name__)

@dns_data_bp.route('/dns-data', methods=['GET'])
@token_required
def get_dns_data(current_user):
    """
    Endpoint para coletar dados DNS de uma API externa (ou Fake API).
    Requer um token válido para autenticação.
    """
    logger.info(f"Usuário '{current_user}' iniciou a requisição para coletar dados DNS.")

    try:
        data = collect_data()
        # Verifica se os dados retornados estão no formato esperado
        if isinstance(data, (dict, list)):
            registros = len(data) if isinstance(data, list) else 1
            logger.info(f"Dados coletados com sucesso. Total de registros: {registros}.")
            return jsonify(data), 200
        else:
            logger.error(f"Formato inválido de dados retornado pela API. Dados recebidos: {data}")
            return jsonify({
                "error": "Invalid data format returned from the data source",
                "details": str(data)
            }), 500

    except Exception as e:
        logger.error(f"Erro ao coletar dados DNS do endpoint: {str(e)}")
        return jsonify({
            "error": "Failed to fetch DNS data",
            "details": str(e)
        }), 500
