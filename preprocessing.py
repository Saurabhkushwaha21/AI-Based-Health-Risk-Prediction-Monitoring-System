import hashlib
import hmac
import logging

import bcrypt
import pandas as pd

logger = logging.getLogger("health_processing_pipeline")


def preprocess_heart(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize categorical heart-disease features without silently inventing values."""
    processed_df = df.copy()

    try:
        if "sex" in processed_df.columns:
            processed_df["sex"] = processed_df["sex"].astype(str).str.strip().str.title().map({"Male": 1, "Female": 0})
        if "exercise_induced_angina" in processed_df.columns:
            processed_df["exercise_induced_angina"] = (
                processed_df["exercise_induced_angina"].astype(str).str.strip().str.title().map({"Yes": 1, "No": 0})
            )
        if "chest_pain_type" in processed_df.columns:
            processed_df["chest_pain_type"] = processed_df["chest_pain_type"].astype(str).str.strip().str.title().map(
                {
                    "Typical Angina": 0,
                    "Atypical Angina": 1,
                    "Non-Anginal Pain": 2,
                    "Asymptomatic": 3,
                }
            )
        if processed_df.isnull().values.any():
            raise ValueError("One or more categorical heart features contain an unsupported value.")
        return processed_df
    except Exception:
        logger.exception("Heart feature preprocessing failed.")
        raise


def _password_material(password: str) -> bytes:
    """Pre-hash to a fixed-length value so bcrypt's 72-byte limit is harmless."""
    return hashlib.sha256(password.encode("utf-8")).digest()


def hash_password(password: str) -> str:
    """Create a bcrypt password hash for new credentials."""
    return bcrypt.hashpw(_password_material(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify bcrypt credentials while retaining safe legacy compatibility."""
    if stored_password.startswith(("$2b$", "$2a$", "$2y$")):
        try:
            return bcrypt.checkpw(_password_material(plain_password), stored_password.encode("utf-8"))
        except ValueError:
            return False

    legacy = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy, stored_password)
