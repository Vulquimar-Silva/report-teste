from src.core.database import db
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum

class ReportStatus(enum.Enum):
    """Enumeração para definir o status do relatório."""
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Report(db.Model):
    """Modelo da tabela `reports` para armazenar informações sobre relatórios gerados."""
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True, index=True)
    client_name = db.Column(db.String, nullable=False, index=True)
    report_path = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False)
    generated_by = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Converte o objeto Report em um dicionário."""
        return {
            "id": self.id,
            "client_name": self.client_name,
            "report_path": self.report_path,
            "status": self.status.value if self.status else None,
            "generated_by": self.generated_by,
            "created_at": (
                self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
            ),
        }
