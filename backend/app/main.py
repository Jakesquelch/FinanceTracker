from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --------------------------
# Database setup
# --------------------------
DATABASE_URL = "sqlite:///./finance.db"  # Later you can swap this for Postgres via .env

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --------------------------
# SQLAlchemy model
# --------------------------
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, index=True)
    amount = Column(Float)
    category = Column(String)
    type = Column(String)  # "income" or "expense"

# --------------------------
# Pydantic schemas
# --------------------------
class TransactionBase(BaseModel):
    description: str
    amount: float
    category: str
    type: str

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

# --------------------------
# App setup
# --------------------------
app = FastAPI()

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Allow Angular frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # ✅ fixed typo from "localhose"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------
# Routes
# --------------------------
@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

@app.post("/transactions", response_model=TransactionRead)
def create_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    db_tx = Transaction(**tx.dict())
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

@app.get("/transactions", response_model=List[TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()
