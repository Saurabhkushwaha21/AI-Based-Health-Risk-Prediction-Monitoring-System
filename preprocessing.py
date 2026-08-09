import hashlib
import hmac
import logging

import pandas as pd

logger = logging.getLogger("health_processing_pipeline")


def preprocess_heart(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize categorical heart-disease features without silently inventing values."""
    processed_df = df.copy()

    try:
        if "sex" in processed_df.columns:
            processed_df["sex"] = (
                processed_df["sex"].astype(str).str.strip().str.title().map({"Male": 1, "Female": 0})
            )

        if "exercise_induced_angina" in processed_df.columns:
            processed_df["exercise_induced_angina"] = (
                processed_df["exercise_induced_angina"]
                .astype(str)
                .str.strip()
                .str.title()
                .map({"Yes": 1, "No": 0})
            )

        if "chest_pain_type" in processed_df.columns:
            processed_df["chest_pain_type"] = (
                processed_df["chest_pain_type"]
                .astype(str)
                .str.strip()
                .str.title()
                .map(
                    {
                        "Typical Angina": 0,
                        "Atypical Angina": 1,
                        "Non-Anginal Pain": 2,
                        "Asymptomatic": 3,
                    }
                )
            )

        if processed_df.isnull().values.any():
            raise ValueError("One or more categorical heart features contain an unsupported value.")

        return processed_df
    except Exception:
        logger.exception("Heart feature preprocessing failed.")
        raise


def hash_password(password: str) -> str:
    """Hash a password for legacy compatibility.

    This project previously used SHA-256. New production deployments should
    migrate to a password KDF such as Argon2id or bcrypt; this function remains
    compatible with existing stored credentials until that migration is made.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Constant-time comparison for the existing password hash format."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)
