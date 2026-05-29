from sqlalchemy import String, create_engine, Column, Integer, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

DATABASE_URL = "sqlite:///./health.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# TABLE
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    diabetes_risk = Column(Float)
    heart_risk = Column(Float)
    overall_risk = Column(Float)
    input_data = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# CREATE TABLE
Base.metadata.create_all(bind=engine)


# DB SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)