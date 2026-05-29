from pydantic import BaseModel, Field
from typing import List

class HeartFeatures(BaseModel):
    # Variables ka naam aur data types bilkul same hain, bas safety constraints (Field) jode hain
    age: int = Field(..., ge=1, le=125, description="Age in years must be realistic (1-125).")
    sex: str = Field(..., description="Categorical biological sex identifier (e.g., 'Male', 'Female').")
    chest_pain_type: str = Field(..., description="Type of clinical chest pain experienced.")
    resting_blood_pressure: float = Field(..., ge=40, le=300, description="Resting blood pressure in mm Hg.")
    cholestoral: float = Field(..., ge=50, le=600, description="Serum cholesterol level measured in mg/dl.")
    fasting_blood_sugar: str = Field(..., description="Fasting blood sugar calculation token.")
    rest_ecg: str = Field(..., description="Resting electrocardiographic diagnostic result category.")
    Max_heart_rate: float = Field(..., ge=50, le=250, description="Maximum heart rate achieved during stress test.")
    exercise_induced_angina: str = Field(..., description="Presence of exercise-induced angina symptoms.")
    oldpeak: float = Field(..., ge=0.0, le=10.0, description="ST depression induced by exercise relative to rest.")
    slope: str = Field(..., description="The slope of the peak exercise ST segment.")
    vessels_colored_by_flourosopy: str = Field(..., description="Number of major vessels colored by fluoroscopy.")
    thalassemia: str = Field(..., description="Thalassemia status classification category.")

    class Config:
        # Swagger UI/OpenAPI schema description auto-documentation ke liye sample payloads
        json_schema_extra = {
            "example": {
                "age": 52,
                "sex": "Male",
                "chest_pain_type": "Typical angina",
                "resting_blood_pressure": 125.0,
                "cholestoral": 212.0,
                "fasting_blood_sugar": "False",
                "rest_ecg": "Normal",
                "Max_heart_rate": 168.0,
                "exercise_induced_angina": "No",
                "oldpeak": 1.0,
                "slope": "Downsloping",
                "vessels_colored_by_flourosopy": "0",
                "thalassemia": "Normal"
            }
        }


class HealthInput(BaseModel):
    # Diabetes data array validation controls aur configuration
    diabetes_features: List[float] = Field(
        ..., 
        min_items=8, 
        max_items=8, 
        description="Must contain exactly 8 continuous numerical values for diabetes vector analysis calculation."
    )
    heart_features: HeartFeatures

    class Config:
        json_schema_extra = {
            "example": {
                "diabetes_features": [6.0, 148.0, 72.0, 35.0, 0.0, 33.6, 0.627, 50.0],
                "heart_features": {
                    "age": 52,
                    "sex": "Male",
                    "chest_pain_type": "Typical angina",
                    "resting_blood_pressure": 125.0,
                    "cholestoral": 212.0,
                    "fasting_blood_sugar": "False",
                    "rest_ecg": "Normal",
                    "Max_heart_rate": 168.0,
                    "exercise_induced_angina": "No",
                    "oldpeak": 1.0,
                    "slope": "Downsloping",
                    "vessels_colored_by_flourosopy": "0",
                    "thalassemia": "Normal"
                }
            }
        }
