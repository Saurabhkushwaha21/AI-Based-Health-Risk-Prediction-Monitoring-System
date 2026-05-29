import numpy as np
import pandas as pd
import pickle

# Load models
with open("models/diabetes.pkl", "rb") as f:
    d_model = pickle.load(f)

with open("models/heart.pkl", "rb") as f:
    h_model = pickle.load(f)


def final_health_prediction(input_data):
    import numpy as np
    import pandas as pd

    # ✅ FIX 1: Diabetes → make 2D
    diabetes_features = np.array(input_data['diabetes_features']).reshape(1, -1)

    # ✅ FIX 2: Heart → convert dict to DataFrame properly
    heart_features = pd.DataFrame([input_data["heart_features"]])

    print("Diabetes:", diabetes_features)
    print("Heart DF:\n", heart_features)

    # Predictions
    diabetes_risk = d_model.predict_proba(diabetes_features)[0][1] * 100
    heart_risk = h_model.predict_proba(heart_features)[0][1] * 100

    overall_risk = (0.4 * diabetes_risk + 0.4 * heart_risk)

    return {
        "Diabetes_Risk (%)": round(diabetes_risk, 2),
        "Heart_Risk (%)": round(heart_risk, 2),
        "Overall_Risk (%)": round(overall_risk, 2)
    }