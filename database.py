import logging
import os
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("health_database_layer")

# Load local environment variables when python-dotenv is available.
if os.path.exists(".env"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logger.warning(".env found but python-dotenv is not installed.")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./health.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    # Nullable keeps existing databases backwards compatible. New records are
    # always associated with the authenticated user in the API layer.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    diabetes_risk = Column(Float, nullable=False, default=0.0)
    heart_risk = Column(Float, nullable=False, default=0.0)
    overall_risk = Column(Float, nullable=False, default=0.0)
    input_data = Column(Text, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


def _ensure_prediction_user_id_column() -> None:
    """Add the ownership column to an existing database without dropping data.

    This lightweight compatibility migration is intentionally limited to the
    new column. Production deployments should use a real migration tool such
    as Alembic for future schema changes.
    """
    inspector = inspect(engine)
    if "predictions" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("predictions")}
    if "user_id" in columns:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE predictions ADD COLUMN user_id INTEGER"))
    logger.info("Added predictions.user_id ownership column to existing database.")


def init_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
        _ensure_prediction_user_id_column()
        logger.info("Database tables verified successfully.")
    except Exception:
        logger.exception("Database initialization failed.")
        raise RuntimeError("Database initialization failed. Check DATABASE_URL and schema configuration.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
