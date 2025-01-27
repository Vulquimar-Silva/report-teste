"""
Inicializa as models do projeto, garantindo que db seja importado antes das classes.
"""

from src.core.database import db  # Importa a instância do SQLAlchemy

# Importa todas as classes de modelo para que Flask-Migrate as enxergue
from src.models.dns_data import DNSData
from src.models.report import Report
from src.models.user import User
