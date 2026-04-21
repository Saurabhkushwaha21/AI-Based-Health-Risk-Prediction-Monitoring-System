from fastapi import FastAPI, Depends
from prediction import final_health_prediction
from fastapi.middleware.cors import CORSMiddleware
from schema import HealthInput
from database import get_db, Prediction
from sqlalchemy.orm import Session
import json
from auth import SECRET_KEY, create_token, verify_password
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from database import get_db, User
from auth import hash_password

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload


@app.get("/")
def home():
    return {"message": "Backend running ✅"}


@app.post("/predict")
def predict(data: HealthInput, db: Session = Depends(get_db)):
    try:
        input_data = {
            "diabetes_features": data.diabetes_features,
            "heart_features": data.heart_features.model_dump()
        }

        result = final_health_prediction(input_data)

        # ✅ SAVE TO DB
        new_entry = Prediction(
            diabetes_risk=result.get("Diabetes_Risk (%)", 0),
            heart_risk=result.get("Heart_Risk (%)", 0),
            overall_risk=result.get("Overall_Risk (%)", 0),
            input_data=json.dumps(input_data)
        )

        db.add(new_entry)
        db.commit()

        return result

    except Exception as e:
        return {"error": str(e)}


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    records = db.query(Prediction).order_by(Prediction.created_at.desc()).all()

    history = []
    for row in records:
        history.append({
            "id": row.id,
            "diabetes_risk": row.diabetes_risk,
            "heart_risk": row.heart_risk,
            "overall_risk": row.overall_risk,
            "input_data": json.loads(row.input_data) if row.input_data else {},
            "date": str(row.created_at)
        })

    return history


@app.delete("/delete/{id}")
def delete_prediction(id: int, db: Session = Depends(get_db)):
    record = db.query(Prediction).filter(Prediction.id == id).first()

    if record:
        db.delete(record)
        db.commit()
        return {"message": "Deleted successfully"}

    return {"error": "Not found"}

#authentication end point
@app.post("/login")
def login(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data["email"]).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(data["password"], user.password):
        return {"error": "Wrong password"}

    token = create_token({"email": user.email})

    return {"access_token": token}

#this is just a dummy register end point, in real application you should use proper database and hashing for passwords
@app.post("/register")
def register(user: dict, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user["password"])

    new_user = User(
        email=user["email"],
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@app.get("/history")
def get_history(user=Depends(verify_token)):
    return {"message": f"Welcome {user['email']}"}