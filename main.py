import json
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

# Saare modules bina kisi badlav ke import ho rahe hain
from schema import HealthInput
from database import get_db, Prediction, init_db, User
from prediction import final_health_prediction, load_ml_models

# Security modules injected without altering existing ones
from preprocessing import hash_password, verify_password
from auth import create_access_token, get_current_user

# Standard Enterprise Production Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("health_api_gateway")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Production Application Lifespan State Manager.
    Synchronizes relational databases and boots heavy ML tensor weight caches directly into system RAM.
    """
    logger.info("🔄 Initializing system infrastructure checks...")
    init_db()
    load_ml_models()
    logger.info("🚀 Health Prediction Backend Engine Started Successfully and Model Caches are Live!")
    yield
    logger.info("🛑 Shutting Down Backend Engine Cleanly...")

app = FastAPI(
    title="AI-Based Health Risk Prediction Engine",
    description="Production-grade API for predicting multi-disease risks securely and concurrently.",
    version="1.0.0",
    lifespan=lifespan
)

# ==========================================
# ENTERPRISE AUDIT LOGGING MIDDLEWARE
# ==========================================
@app.middleware("http")
async def audit_logging_middleware(request, call_next):
    """
    Tracks network request endpoints, incoming methods, status response structures, 
    and microsecond performance evaluation logs for infrastructure health auditing.
    """
    start_time = time.time()
    
    # Process incoming request pipeline
    response = await call_next(request)
    
    # Calculate operational processing latency
    process_time = (time.time() - start_time) * 1000
    
    logger.info(
        f"Method: {request.method} | Path: {request.url.path} | "
        f"Status: {response.status_code} | Latency: {process_time:.2f}ms"
    )
    return response

# =========================
# CORS MIDDLEWARE SECURED
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ai-based-health-risk-prediction.netlify.app"],  # Production ke waqt yahan apna Netlify URL daliyega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inbound Identity Data Contracts
class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    """Server status check endpoint."""
    return {"status": "healthy", "message": "Backend is online and running ✅"}


# ==========================================
# AUTHENTICATION API ENDPOINTS
# ==========================================
@app.post("/api/v1/auth/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    """Registers a brand new secure operator profile using secure cryptographic hashing."""
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="This email address is already registered in our system."
        )
        
    new_user = User(
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    return {"status": "success", "message": "User security account created successfully."}


@app.post("/api/v1/auth/login", status_code=status.HTTP_200_OK)
async def login(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    """Verifies profile credentials and issues a cryptographic secure bearer session token."""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credential records mapping provided."
        )
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "email": user.email}


# =========================
# PREDICTION API (Asynchronous & Safe)
# =========================
@app.post("/predict", status_code=status.HTTP_201_CREATED)
async def predict(data: HealthInput, db: Session = Depends(get_db)):
    """
    Accepts patient vitals, triggers the ML prediction layer, 
    persists input/results to the database asynchronously, and returns evaluation data.
    """
    try:
        input_data = {
            "diabetes_features": data.diabetes_features,
            "heart_features": data.heart_features.model_dump()
        }

        result = final_health_prediction(input_data)

        new_entry = Prediction(
            diabetes_risk=result.get("Diabetes_Risk (%)", 0),
            heart_risk=result.get("Heart_Risk (%)", 0),
            overall_risk=result.get("Overall_Risk (%)", 0),
            input_data=json.dumps(input_data)
        )

        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return result

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An internal error occurred during processing: {str(e)}"
        )


# =========================
# HISTORY API (Secured)
# =========================
@app.get("/history", status_code=status.HTTP_200_OK)
async def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetches diagnostic prediction historical analytics strictly for logged-in authentication profiles."""
    try:
        records = db.query(Prediction).order_by(Prediction.created_at.desc()).all()

        return [
            {
                "id": r.id,
                "diabetes_risk": r.diabetes_risk,
                "heart_risk": r.heart_risk,
                "overall_risk": r.overall_risk,
                "input_data": json.loads(r.input_data) if isinstance(r.input_data, str) else r.input_data,
                "date": str(r.created_at)
            }
            for r in records
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch records: {str(e)}"
        )


# =========================
# DELETE API (Secured)
# =========================
@app.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_prediction(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Securely purges matching identification records tracking execution safety locks."""
    record = db.query(Prediction).filter(Prediction.id == id).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record with ID {id} does not exist in our systems."
        )

    try:
        db.delete(record)
        db.commit()
        return {"status": "success", "message": f"Record {id} successfully purged from storage."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database execution failed on deletion: {str(e)}"
        )
