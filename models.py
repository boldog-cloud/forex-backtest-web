from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from config import SQLALCHEMY_DATABASE_URI
from datetime import datetime

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class Trade(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    position = Column(String(10), nullable=False)  # LONG / SHORT
    entry_reason = Column(String(500), nullable=True)
    profit = Column(Float, nullable=False)  # profit in account currency
    win = Column(String(10), nullable=False)  # WIN / LOSS
    balance_after = Column(Float, nullable=False)

def init_db():
    Base.metadata.create_all(engine)
