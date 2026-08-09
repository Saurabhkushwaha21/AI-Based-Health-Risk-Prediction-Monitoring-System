# 🩺 AI-Based Health Risk Prediction & Monitoring System

A full-stack healthcare application that combines **machine-learning prediction services, FastAPI REST APIs, authentication, database persistence, and a responsive web interface** for preventive health-risk analysis.

> **Important:** This is an educational/portfolio project. Predictions are not medical diagnoses and should not be used as a substitute for a qualified healthcare professional.

## 🎯 Core capabilities

- Diabetes-risk prediction
- Heart-disease risk prediction
- Authenticated prediction history
- REST API integration
- ML model inference using Python
- SQLAlchemy database persistence
- Responsive HTML/CSS/JavaScript frontend
- Environment-based backend configuration

## 🏗 Architecture

```text
Browser UI
   │
   ▼
FastAPI REST API
   │
   ├── Authentication / JWT
   │
   ├── Prediction service
   │      ├── Diabetes model
   │      └── Heart-risk model
   │
   └── SQLAlchemy
          │
          ▼
       Database
```

## 🛠 Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | MySQL / SQLite for local development |
| ML | scikit-learn, Pandas, NumPy |
| Authentication | JWT bearer tokens |

## 🔐 Security principles

- Passwords are stored as hashes, never as plaintext.
- JWT signing secrets are provided through environment variables.
- Prediction history is associated with the authenticated user.
- Prediction deletion verifies record ownership.
- Production CORS origins should be explicitly configured.
- Internal exception details are logged server-side rather than returned to clients.
- Real credentials must never be committed to Git.

## 🧠 Machine Learning

The application loads trained models and returns risk scores for supported health inputs.

For reproducible ML evaluation, document the exact model, dataset, preprocessing pipeline, train/test split, and metrics used for each model. The API layer should not be treated as evidence of model accuracy by itself.

## 📡 API

Typical endpoints:

```text
POST /api/v1/auth/signup
POST /api/v1/auth/login
POST /predict
GET  /history
DELETE /delete/{prediction_id}
GET  /
```

Interactive API documentation is available through FastAPI at `/docs` when the backend is running.

## 🚀 Local setup

```bash
git clone https://github.com/Saurabhkushwaha21/AI-Based-Health-Risk-Prediction-Monitoring-System.git
cd AI-Based-Health-Risk-Prediction-Monitoring-System
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and provide a strong `JWT_SECRET_KEY` plus your database configuration.

Run the API from the directory containing the active `main.py`:

```bash
uvicorn main:app --reload
```

## 🧪 Quality checklist

Before publishing a new release, verify:

```text
✓ Registration and login
✓ Invalid-token rejection
✓ User A cannot read User B history
✓ User A cannot delete User B prediction
✓ Prediction validation
✓ Database rollback on failures
✓ Frontend API authentication flow
✓ No secrets committed
```

## 📸 Screenshots

Existing application screenshots are included in the repository. Add future screenshots under `docs/screenshots/` with descriptive names rather than placeholder filenames.

## 🔭 Future improvements

- Argon2id/bcrypt password-hash migration for legacy credentials
- Alembic-managed schema migrations
- Automated API/integration test suite
- Model versioning and reproducible training pipeline
- ML evaluation dashboard with precision/recall/F1/ROC-AUC
- Rate limiting and audit logging
- Production observability

## 💼 Resume-ready summary

**AI-Based Health Risk Prediction & Monitoring System** — Built a full-stack health-risk application using Python, FastAPI, SQLAlchemy, MySQL/SQLite, JavaScript and scikit-learn, integrating authenticated ML predictions with user-specific history and REST APIs.

## 👨‍💻 Author

**Saurabh Kushwaha** — B.Tech Artificial Intelligence & Machine Learning

- GitHub: https://github.com/Saurabhkushwaha21
- LinkedIn: https://www.linkedin.com/in/saurabh-kushwaha-8b7a56293/
