from flask import Blueprint, jsonify
from src.core.config import SessionLocal
from src.models.report import Report

internal_report_bp = Blueprint('internal_report', __name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@internal_report_bp.route("/internal-reports", methods=["GET"])
def read_internal_reports():
    db = next(get_db())
    reports = db.query(Report).all()
    return jsonify([report.__dict__ for report in reports])
