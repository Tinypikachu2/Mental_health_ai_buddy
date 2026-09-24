from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class APIToken(Base):
    __tablename__ = "api_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_key = Column(String, unique=True, index=True)
    owner_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    logs = relationship("UsageLog", back_populates="token")

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey("api_tokens.id"))
    endpoint = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    token = relationship("APIToken", back_populates="logs")
