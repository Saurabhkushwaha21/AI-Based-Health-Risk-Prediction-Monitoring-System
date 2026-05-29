from pydantic import BaseModel
from typing import List

class HeartFeatures(BaseModel):
    age: int
    sex: str
    chest_pain_type: str
    resting_blood_pressure: float
    cholestoral: float   
    fasting_blood_sugar: str
    rest_ecg: str
    Max_heart_rate: float   
    exercise_induced_angina: str
    oldpeak: float
    slope: str
    vessels_colored_by_flourosopy: str
    thalassemia: str


class HealthInput(BaseModel):
    diabetes_features: List[float]
    heart_features: HeartFeatures