import pandas as pd
import logging
import hashlib

logger = logging.getLogger("health_processing_pipeline")

def preprocess_heart(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes categorical raw text data from inputs into numerical matrix vectors.
    Contains fallback mechanisms for casing disparities and missing fields to prevent ML runtime crashes.
    """
    # Variable bilkul badla nahi hai, copy() lene se memory lock secure ho jati hai (No Mutation Risk)
    processed_df = df.copy()

    try:
        # 1. Sex Category Mapping (Safe Alignment)
        # Case-insensitivity support ke liye .str.strip().str.title() lagaya hai taaki 'male' ya 'Male' dono sahi se 1 bane
        if "sex" in processed_df.columns and processed_df["sex"].dtype == object:
            processed_df["sex"] = processed_df["sex"].str.strip().str.title().map({"Male": 1, "Female": 0})
        else:
            processed_df["sex"] = processed_df["sex"].map({"Male": 1, "Female": 0})

        # 2. Exercise Induced Angina Mapping (Safe Alignment)
        if "exercise_induced_angina" in processed_df.columns and processed_df["exercise_induced_angina"].dtype == object:
            processed_df["exercise_induced_angina"] = processed_df["exercise_induced_angina"].str.strip().str.title().map({"Yes": 1, "No": 0})
        else:
            processed_df["exercise_induced_angina"] = processed_df["exercise_induced_angina"].map({"Yes": 1, "No": 0})

        # 3. Chest Pain Type Mapping (Safe Alignment)
        if "chest_pain_type" in processed_df.columns and processed_df["chest_pain_type"].dtype == object:
            processed_df["chest_pain_type"] = processed_df["chest_pain_type"].str.strip().str.title().map({
                "Typical Angina": 0,
                "Atypical Angina": 1,
                "Non-Anginal Pain": 2,
                "Asymptomatic": 3
            })
        else:
            processed_df["chest_pain_type"] = processed_df["chest_pain_type"].map({
                "Typical angina": 0,
                "Atypical angina": 1,
                "Non-anginal pain": 2,
                "Asymptomatic": 3
            })

        # 🚨 Zero-Crash Check: Agar koi value map nahi ho payi aur NaN ban gayi, toh fallback default values lagana mandatory hai
        # Taaki aapka ML model (.predict_proba) kabhi bhi NaN matrix data dekh kar crash na ho
        if processed_df.isnull().values.any():
            logger.warning("Pipeline found unresolved or unmapped strings. Applying safety fallback values.")
            processed_df["sex"] = processed_df["sex"].fillna(1)  # Default Fallback to Male
            processed_df["exercise_induced_angina"] = processed_df["exercise_induced_angina"].fillna(0)  # Default Fallback to No
            processed_df["chest_pain_type"] = processed_df["chest_pain_type"].fillna(0)  # Default Fallback to Typical Angina

        return processed_df

    except Exception as e:
        logger.error(f"Data transformation pipeline failed during categorical mapping calculation: {str(e)}")
        raise RuntimeError(f"Data mapping transformation subsystem failure: {str(e)}")


def hash_password(password: str) -> str:
    """Secures raw user passwords using SHA-256 secure cryptographic hashing before saving to database."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies inbound user input password strings against persisted cryptographic database hashes."""
    return hash_password(plain_password) == hashed_password