import logging
import pickle
import numpy as np
import pandas as pd

# Standard Production Logging Configuration
logger = logging.getLogger("health_prediction_engine")

# Global Cache Storage Models ko RAM me rakhne ke liye
_DIABETES_MODEL = None
_HEART_MODEL = None

def load_ml_models():
    """
    Explicitly loads machine learning models from storage artifacts into RAM memory.
    This architecture prevents unexpected hard-disk I/O operations during file imports.
    """
    global _DIABETES_MODEL, _HEART_MODEL
    
    # Singleton Pattern: Agar model pehle se loaded hai toh dobara load mat karo
    if _DIABETES_MODEL is not None and _HEART_MODEL is not None:
        return
        
    try:
        logger.info("Initializing heavy Machine Learning model artifacts into RAM...")
        with open("models/diabetes.pkl", "rb") as f:
            _DIABETES_MODEL = pickle.load(f)
            
        with open("models/heart.pkl", "rb") as f:
            _HEART_MODEL = pickle.load(f)
            
        logger.info("🚀 System Memory Sync Complete: All ML models are live in RAM cache.")
    except FileNotFoundError as e:
        logger.critical(f"Fatal System Boot Error: Verification failed for ML artifact paths. Details: {str(e)}")
        raise RuntimeError(f"Critical deployment files are missing from disk space: {str(e)}")
    except Exception as e:
        logger.critical(f"Unexpected memory corruption during pipeline parsing: {str(e)}")
        raise RuntimeError(f"Failed to bootstrap pipeline assets cleanly: {str(e)}")


def final_health_prediction(input_data):
    """
    Processes client parameters, standardizes vector arrays, 
    and executes isolated model predictions concurrently with zero disk dependencies.
    """
    global _DIABETES_MODEL, _HEART_MODEL

    # Lazy-loading safety fallback block
    if _DIABETES_MODEL is None or _HEART_MODEL is None:
        load_ml_models()

    try:
        # ✅ Aapka asli transformations logic bilkul change nahi kiya gaya hai
        # Diabetes Vector Alignment → 2D Formatter
        diabetes_features = np.array(input_data['diabetes_features']).reshape(1, -1)

        # Heart Structural Conversion → Structural DataFrame Formatter
        heart_features = pd.DataFrame([input_data["heart_features"]])

        # Model Inference Pipeline Calculations (Thread-Safe Evaluation)
        diabetes_prob = _DIABETES_MODEL.predict_proba(diabetes_features)[0][1]
        heart_prob = _HEART_MODEL.predict_proba(heart_features)[0][1]

        # Scaled Analytics Engine (Percentage Scalers)
        diabetes_risk = diabetes_prob * 100
        heart_risk = heart_prob * 100

        # Overall Risk Formula Configuration
        overall_risk = (0.4 * diabetes_risk + 0.4 * heart_risk)

        return {
            "Diabetes_Risk (%)": round(diabetes_risk, 2),
            "Heart_Risk (%)": round(heart_risk, 2),
            "Overall_Risk (%)": round(overall_risk, 2)
        }

    except KeyError as e:
        logger.error(f"Inbound Request Schema Validation Breach: Parameter {str(e)} missing from contract payload.")
        raise ValueError(f"Malformed input contract payload map. Missing criteria token: {str(e)}")
        
    except Exception as e:
        logger.error(f"Execution engine failure under operational stress. Matrix trace: {str(e)}")
        raise RuntimeError(f"The calculation sub-processor failed to infer probabilities: {str(e)}")
