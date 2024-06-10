from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Anomaly(Base):
    __tablename__ = 'anomalies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(String)
    event_id = Column(String, index=True)
    role_id = Column(String)
    event_type = Column(String)
    event_timestamp = Column(DateTime, default=datetime.utcnow)
    affected_assets = Column(ARRAY(String))
    score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return (f"<Anomaly(id={self.id}, request_id={self.request_id}, event_id={self.event_id}, "
                f"role_id={self.role_id}, event_type={self.event_type}, event_timestamp={self.event_timestamp}, "
                f"affected_assets={self.affected_assets}, score={self.score}, created_at={self.created_at}, "
                f"updated_at={self.updated_at})>")