from fastapi import FastAPI, Depends
from prediction import final_health_prediction
from fastapi.middleware.cors import CORSMiddleware
from schema import HealthInput
from database import get_db, Prediction
from sqlalchemy.orm import Session
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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