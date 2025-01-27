# Se você tem algo assim:
from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError
from src.core.logger import logger
from src.models.report import Report
# Aqui você importa a instância global do db
from src.core.database import db 

internal_report_bp = Blueprint('internal_report', __name__)

@internal_report_bp.route("/internal-reports", methods=["GET"])
def read_internal_reports():
    logger.info("Iniciando requisição para obter relatórios internos.")
    try:
        # Em Flask-SQLAlchemy, você pode usar:
        reports = Report.query.all()
        result = [rep.to_dict() for rep in reports]
        return jsonify(result), 200

    except SQLAlchemyError as e:
        logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
        return jsonify({"error": "Failed to fetch internal reports", "details": str(e)}), 500
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
