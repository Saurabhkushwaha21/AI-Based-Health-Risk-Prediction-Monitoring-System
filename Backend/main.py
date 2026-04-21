from fastapi import FastAPI
from prediction import final_health_prediction
from fastapi.middleware.cors import CORSMiddleware
from schema import HealthInput

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

        # ❌ DB removed temporarily
        print("Prediction:", result)

        return result

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}


@app.get("/history")
def get_history():
    return []   # temporary


@app.delete("/delete/{id}")
def delete_prediction(id: int):
    return {"message": "Deleted successfully"}