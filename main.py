import json
import logging
import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user
from database import Prediction, User, get_db, init_db
from prediction import final_health_prediction, load_ml_models
from preprocessing import hash_password, verify_password
from schema import HealthInput

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("health_api")

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "https://ai-based-health-risk-prediction.netlify.app").split(",")
    if origin.strip()
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    load_ml_models()
    logger.info("Health prediction API started.")
    yield
    logger.info("Health prediction API stopped.")


app = FastAPI(title="AI-Based Health Risk Prediction API", version="1.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"status": "healthy", "message": "Backend is online"}


@app.post("/api/v1/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    email = str(user_data.email).lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Email is already registered.")

    user = User(email=email, password=hash_password(user_data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"status": "success", "message": "User registered successfully."}


@app.post("/api/v1/auth/login", status_code=status.HTTP_200_OK)
async def login(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    email = str(user_data.email).lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Transparently upgrade legacy SHA-256 credentials after a successful login.
    if not user.password.startswith(("$2b$", "$2a$", "$2y$")):
        user.password = hash_password(user_data.password)
        db.commit()

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "email": user.email}


@app.post("/predict", status_code=status.HTTP_201_CREATED)
async def predict(
    data: HealthInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        input_data = {
            "diabetes_features": data.diabetes_features,
            "heart_features": data.heart_features.model_dump(),
        }
        result = final_health_prediction(input_data)
        new_entry = Prediction(
            user_id=current_user.id,
            diabetes_risk=float(result.get("Diabetes_Risk (%)", 0)),
            heart_risk=float(result.get("Heart_Risk (%)", 0)),
            overall_risk=float(result.get("Overall_Risk (%)", 0)),
            input_data=json.dumps(input_data),
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return result
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        logger.exception("Prediction request failed: %s", exc)
        raise HTTPException(status_code=500, detail="Prediction service temporarily unavailable.") from exc


@app.get("/history", status_code=status.HTTP_200_OK)
async def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        records = (
            db.query(Prediction)
            .filter(Prediction.user_id == current_user.id)
            .order_by(Prediction.created_at.desc())
            .all()
        )
        return [
            {
                "id": record.id,
                "diabetes_risk": record.diabetes_risk,
                "heart_risk": record.heart_risk,
                "overall_risk": record.overall_risk,
                "input_data": json.loads(record.input_data),
                "date": record.created_at.isoformat(),
            }
            for record in records
        ]
    except Exception as exc:
        logger.exception("History request failed: %s", exc)
        raise HTTPException(status_code=500, detail="Unable to fetch prediction history.") from exc


@app.delete("/delete/{prediction_id}", status_code=status.HTTP_200_OK)
async def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    record = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id, Prediction.user_id == current_user.id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=404, detail="Prediction not found.")

    try:
        db.delete(record)
        db.commit()
        return {"status": "success", "message": "Prediction deleted successfully."}
    except Exception as exc:
        db.rollback()
        logger.exception("Prediction deletion failed: %s", exc)
        raise HTTPException(status_code=500, detail="Unable to delete prediction.") from exc
