from fastapi import FastAPI
from prediction import final_health_prediction
from database import cursor
from fastapi.middleware.cors import CORSMiddleware
from schema import HealthInput
import json
from database import cursor, conn 

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
def predict(data: HealthInput):
    try:
        input_data = {
            "diabetes_features": data.diabetes_features,
            "heart_features": data.heart_features.model_dump()
        }

        result = final_health_prediction(input_data)

        cursor.execute("""
            INSERT INTO predictions 
            (diabetes_risk, heart_risk, overall_risk, input_data)
            VALUES (%s, %s, %s, %s)
        """, (
            result.get("Diabetes_Risk (%)", 0),
            result.get("Heart_Risk (%)", 0),
            result.get("Overall_Risk (%)", 0),
            json.dumps(input_data)   # 🔥 important
        ))

        conn.commit()

        print("DATA INSERTED ✅")   # debug

        return result

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}


@app.get("/history")
def get_history():
    cursor.execute("""
    SELECT id, diabetes_risk, heart_risk, overall_risk, input_data, created_at
    FROM predictions
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "diabetes_risk": row[1],
            "heart_risk": row[2],
            "overall_risk": row[3],
            "input_data": json.loads(row[4]) if row[4] else {},
            "date": str(row[5])
        })

    return history

# DELETE PREDICTION
@app.delete("/delete/{id}")
def delete_prediction(id: int):
    cursor.execute("DELETE FROM predictions WHERE id = %s", (id,))
    cursor.connection.commit()
    return {"message": "Deleted successfully"}