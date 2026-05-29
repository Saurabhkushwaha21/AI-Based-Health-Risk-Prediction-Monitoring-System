import os
import logging
from datetime import datetime, timezone
from sqlalchemy import String, create_engine, Column, Integer, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("health_database_layer")

# AUTOMATED ENVIRONMENT LOADER BLOCK
# Agar local par chala rahe hain, toh yeh .env file ko read karega automatically
if os.path.exists(".env"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning(".env file detected but python-dotenv is not installed. Skipping environment file load.")

# 1. Configurable Connection Contract (.env se database url check karega safely)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health.db")

# Connection Pool Settings optimized for highly concurrent product demands
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
else:
    # Enterprise configs (PostgreSQL/MySQL instance manager fallbacks)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==========================================
# TABLE: PREDICTION (Columns remain 100% Same)
# ==========================================
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    diabetes_risk = Column(Float)
    heart_risk = Column(Float)
    overall_risk = Column(Float)
    input_data = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ==========================================
# TABLE: USER (Columns remain 100% Same)
# ==========================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)


# ==========================================
# DATA INITIATION & ISOLATED MANAGEMENT
# ==========================================
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Core relational tables verified and synchronized successfully.")
    except Exception as e:
        logger.critical(f"Database bootstrap layer failed to initialize models: {str(e)}")
        raise RuntimeError(f"Database structural handshake error: {str(e)}")


# DB SESSION CONTEXT
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session boundary exception intercepted. Rolling back: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
