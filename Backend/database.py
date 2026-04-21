'''import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh@123",
    database="health_db"
)
cursor = conn.cursor()'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()