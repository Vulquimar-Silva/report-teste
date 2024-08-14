from sqlalchemy import Column, Integer, String, DateTime
from src.core.config import Base
from datetime import datetime

class Report(Base):
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    report_path = Column(String)
    status = Column(String)
    generated_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
