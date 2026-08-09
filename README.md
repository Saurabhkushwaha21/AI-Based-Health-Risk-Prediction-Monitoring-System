# 🩺 AI-Based Health Risk Prediction & Monitoring System

> A full-stack machine-learning project that connects health-data input, disease-risk prediction, authenticated APIs, and prediction history.

## Why I Built This

I built this project to understand how a machine-learning model can be integrated into a usable software application. Instead of keeping prediction code separate, the project connects the ML workflow with a FastAPI backend, database persistence, authentication, and a browser-based frontend.

## Key Features

- 🤖 Diabetes and heart-disease risk prediction workflows
- 📈 Risk probability/output presentation
- 🔐 JWT-based authentication and protected APIs
- 👤 User-specific prediction history
- 🗄️ MySQL persistence through SQLAlchemy
- 🌐 REST API built with FastAPI
- 🖥️ HTML/CSS/JavaScript frontend
- ✅ Input validation with Pydantic
- 🧪 Backend testing and API validation

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | MySQL |
| Machine Learning | Scikit-learn, Pandas, NumPy |
| Authentication | JWT, password hashing |

## Architecture

```text
Browser UI
    │
    ▼
HTML / CSS / JavaScript
    │
    │ REST API
    ▼
FastAPI Backend
    │
 ┌──┴───────────────┐
 ▼                  ▼
Authentication   ML Prediction
 │                  │
 ▼                  ▼
MySQL          Trained Models
 │
 ▼
Prediction History
```

## Machine Learning Workflow

```text
User Health Parameters
          │
          ▼
Input Validation
          │
          ▼
Preprocessing
          │
          ▼
Trained ML Model
          │
          ▼
Risk Prediction
          │
          ▼
Authenticated History
```

The repository contains ML models/workflows for health-risk prediction. Model quality should be evaluated against the actual dataset and evaluation code; this README intentionally does not claim unsupported accuracy numbers.

## Authentication & Authorization

The application uses backend authentication rather than treating browser-side state as the source of truth.

- Passwords are hashed before storage.
- JWTs protect authenticated API operations.
- Prediction history is scoped to the authenticated user.
- Users cannot access another user's prediction records through the API.
- Protected delete/history operations enforce ownership.
- Secrets are configured through environment variables rather than committed credentials.

## API Capabilities

The backend provides functionality around:

- User registration
- User login
- Authenticated prediction requests
- Prediction history
- User-owned prediction management

Run the backend and use FastAPI's interactive documentation to inspect the exact current routes and request/response schemas.

## Project Structure

```text
.
├── backend/          # FastAPI app, auth, database and ML integration
├── frontend/         # HTML/CSS/JavaScript UI
├── .github/          # CI/test automation where configured
├── README.md
└── .gitignore
```

## Run Locally

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Configure the required environment variables using the repository's example configuration. Never commit real database credentials or JWT secrets.

Start the backend with the project's FastAPI entry point, for example:

```bash
uvicorn main:app --reload
```

When running, FastAPI exposes interactive API documentation at `/docs` if enabled by the application configuration.

Open the frontend from the repository's frontend files using the development setup documented by the project.

## Testing

The project should be validated at both API and application levels. Typical backend testing command:

```bash
pytest
```

Security-sensitive tests cover areas such as:

- Authentication
- Invalid credentials
- Protected prediction requests
- Prediction ownership
- History access
- Delete authorization
- Request validation

## Security

- JWT authentication
- Password hashing
- Protected API routes
- User ownership checks
- Pydantic request validation
- Environment-based secrets
- Safe API error handling
- Database transaction handling on failures

## Screenshots

The repository includes application screenshots demonstrating the current UI.

For a portfolio presentation, keep screenshots focused on:

- Login / registration
- Prediction form
- Prediction result
- User history/dashboard

## Medical Disclaimer

**This project is an educational machine-learning application and is not a medical diagnostic tool.** Predictions are model outputs and should not be used as a substitute for professional medical advice, diagnosis, or treatment.

## Engineering Challenges

This project gave me practical experience with:

- Integrating ML inference into a REST API
- Designing authenticated prediction workflows
- Persisting user-specific prediction history
- Enforcing authorization and ownership
- Validating ML inputs before inference
- Connecting a browser frontend with FastAPI
- Testing security-sensitive API behavior

## Known Limitations

This is a portfolio/learning project. Prediction quality depends on the training data and model evaluation. The application should not be presented as clinically validated software.

## Future Improvements

- Add stronger model evaluation and experiment tracking
- Expand the supported conditions/models
- Add explainability such as feature importance where appropriate
- Improve automated integration/security coverage
- Add richer monitoring and model-version management
- Add production-grade deployment and observability

## Resume Highlights

- Built a full-stack health-risk prediction application integrating Scikit-learn models with FastAPI and MySQL.
- Implemented JWT authentication and user-owned prediction history.
- Connected a browser-based frontend to authenticated ML prediction APIs.
- Added input validation and security-focused API tests.

## Author

**Saurabh Kushwaha**  
B.Tech — Artificial Intelligence & Machine Learning

GitHub: [Saurabhkushwaha21](https://github.com/Saurabhkushwaha21)

LinkedIn: [Saurabh Kushwaha](https://www.linkedin.com/in/saurabh-kushwaha-8b7a56293/)

---

⭐ This repository is maintained as a portfolio project demonstrating practical machine-learning integration and software engineering skills.
