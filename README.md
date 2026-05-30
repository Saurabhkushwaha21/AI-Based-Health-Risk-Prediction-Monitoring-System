# AI-Based Health Risk Prediction & Monitoring System

## Overview

AI-Based Health Risk Prediction & Monitoring System is a full-stack healthcare intelligence platform designed to predict potential health risks using Machine Learning models. The system analyzes user health parameters and provides real-time disease risk predictions for conditions such as Diabetes and Heart Disease.

The platform combines Artificial Intelligence, FastAPI backend services, secure authentication, and interactive dashboards to deliver an efficient and scalable healthcare monitoring solution.

---

# Features

## Core Functionalities

* AI-powered disease risk prediction
* Real-time health analysis
* Secure user authentication and authorization
* Prediction history tracking
* REST API integration
* Interactive and responsive frontend
* Fast and scalable backend architecture
* Machine Learning model integration
* Health monitoring dashboard
* User-friendly UI/UX

---

# Machine Learning Capabilities

The system uses trained Machine Learning models to:

* Predict Diabetes Risk
* Predict Heart Disease Risk
* Analyze health parameters
* Generate risk probability scores
* Provide instant prediction responses

---

# Tech Stack

## Frontend

* HTML5
* CSS3
* JavaScript

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

## Database

* MYSQL

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## Deployment

* Netlify (Frontend)
* Render / Railway / AWS / Docker (Backend)

---

# System Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
REST API Communication
        ↓
FastAPI Backend
        ↓
ML Prediction Engine
        ↓
Database Storage
```

---

# API Features

* User Registration API
* Login Authentication API
* Disease Prediction API
* User History API
* Health Data Management API

---

# Project Structure

```text
AI-Based-Health-Risk-Prediction-Monitoring-System/
│
├── backend/
│   ├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── database/
│   ├── ml_models/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── README.md
└── .gitignore
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/Saurabhkushwaha21/AI-Based-Health-Risk-Prediction-Monitoring-System.git
```

## Navigate to Project

```bash
cd AI-Based-Health-Risk-Prediction-Monitoring-System
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Backend Server

```bash
uvicorn main:app --reload
```

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Future Enhancements

* AI-based symptom checker
* Voice-enabled virtual health assistant
* Real-time patient monitoring
* Wearable device integration
* Emotion-aware disease prediction
* Gut microbiome analysis integration
* Cloud deployment scalability
* Advanced analytics dashboard

---

# Performance Highlights

* Optimized FastAPI backend for high performance
* Scalable REST API architecture
* Secure authentication workflow
* Responsive frontend design
* Efficient ML model integration
* Clean modular project structure

---

# Use Cases

* Healthcare Monitoring
* Disease Risk Assessment
* Preventive Healthcare Systems
* AI-based Medical Assistance
* Health Analytics Platforms
* Smart Healthcare Applications

---

# Security Features

* JWT Authentication
* Password Hashing
* Secure API Access
* Input Validation using Pydantic
* Database Security Practices

---

# Screenshots
<img width="1891" height="910" alt="Screenshot 2026-04-21 230620" src="https://github.com/user-attachments/assets/849d7b23-d210-4163-8d5a-7d940ed98640" />
<img width="1883" height="906" alt="Screenshot 2026-04-21 230734" src="https://github.com/user-attachments/assets/baca5f3e-2228-4d09-b884-b1641cba61b5" />
<img width="1867" height="901" alt="Screenshot 2026-04-21 230900" src="https://github.com/user-attachments/assets/b0d8ab13-a54c-4c3e-b07f-7c2d6da6c1aa" />


```text
assets/screenshots/
```

---

# Deployment

## Frontend Deployment

Deploy frontend using:

* Netlify
* Vercel

## Backend Deployment

Deploy backend using:

* Render
* Railway
* AWS
* Docker

---

# Author

## Saurabh Kushwaha
* Full Stack Developer

GitHub: [https://github.com/Saurabhkushwaha21](https://github.com/Saurabhkushwaha21)

LinkedIn: [https://www.linkedin.com/in/saurabh-kushwaha-8b7a56293/](https://www.linkedin.com/in/saurabh-kushwaha-8b7a56293/)

---

# Resume Highlights

* Developed AI-powered disease prediction platform
* Built scalable FastAPI REST APIs
* Integrated Machine Learning models with backend
* Designed secure authentication system
* Created responsive frontend architecture
* Implemented real-time health prediction workflows

---

# License

This project is licensed under the MIT License.

---

# Conclusion

AI-Based Health Risk Prediction & Monitoring System demonstrates the practical implementation of Artificial Intelligence in healthcare technology. The project showcases Full Stack Development, Machine Learning Integration, REST API Development, Authentication Systems, and Scalable Software Architecture suitable for real-world healthcare applications.
