from flask import Blueprint, jsonify
from src.core.security import token_required
from src.api.services.data_collector import collect_data

dns_data_bp = Blueprint('dns_data', __name__)

@dns_data_bp.route('/dns-data', methods=['GET'])
@token_required
def get_dns_data(current_user):
    data = collect_data()
    return jsonify(data)
