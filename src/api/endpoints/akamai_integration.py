from flask import Blueprint, jsonify, request
import requests
from src.core.security import token_required
from src.core.config import config

akamai_bp = Blueprint('akamai', __name__)

@akamai_bp.route('/akamai/data', methods=['GET'])
@token_required
def get_akamai_data(current_user):
    headers = {
        'Authorization': f"Bearer {config.AKAMAI_API_TOKEN}",
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{config.AKAMAI_API_URL}/endpoint", headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to retrieve data from Akamai'}), response.status_code
