# 🧠 AI-Based Health Risk Prediction & Monitoring System

An intelligent full-stack web application that predicts **Diabetes Risk** and **Heart Disease Risk** using machine learning models.
It provides users with real-time health insights, history tracking, and personalized recommendations.

---

## 🚀 Features

* 🔐 User Authentication (Register / Login / Forgot Password)
* 📊 Health Risk Prediction (Diabetes + Heart Disease)
* 📈 Dashboard with Risk Visualization
* 🧾 History Tracking (View/Delete Past Results)
* 📄 Report Generation (Latest Health Summary)
* 🎯 Personalized Health Recommendations
* 💻 Responsive UI (Mobile + Desktop Friendly)

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI

### Machine Learning

* Scikit-learn
* Pandas
* NumPy

### Storage

* LocalStorage (Frontend)
* Backend Database (optional/extendable)

---

## 📂 Project Structure

```
AI-Based-Health-Risk-Prediction-Monitoring-System/
│
├── Backend/
│   ├── main.py
│   ├── prediction.py
│   ├── preprocessing.py
│   ├── database.py
│   ├── schema.py
│   └── models/
│
├── Frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
└── README.md
```

---

## ⚙️ How to Run Locally

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Based-Health-Risk-Prediction-Monitoring-System.git
cd AI-Based-Health-Risk-Prediction-Monitoring-System
```

---

### 🔹 2. Setup Backend

```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend will run at:
👉 http://127.0.0.1:8000

---

### 🔹 3. Run Frontend

Open:

```
Frontend/index.html
```

in your browser

---

## 🔌 API Endpoints

| Endpoint       | Method | Description          |
| -------------- | ------ | -------------------- |
| `/predict`     | POST   | Predict health risks |
| `/history`     | GET    | Get past predictions |
| `/delete/{id}` | DELETE | Delete a record      |

---

## 📊 Input Parameters

### Diabetes Model

* Pregnancies
* Glucose
* Blood Pressure
* Skin Thickness
* Insulin
* BMI
* Diabetes Pedigree Function
* Age

### Heart Disease Model

* Age, Gender
* Chest Pain Type
* Blood Pressure
* Cholesterol
* ECG Results
* Max Heart Rate
* Exercise Induced Angina
* etc.

---

## 📸 Screenshots (Optional)

*Add screenshots here for better presentation*

---

## 🌐 Deployment

You can deploy using:

* Netlify (Frontend)
* Render / HuggingFace Spaces (Backend)
* Docker (Full Stack)

---

## 🧠 Future Improvements

* 🔔 Email Alerts for High Risk
* 📱 Mobile App Version
* ☁️ Cloud Database Integration
* 🤖 More Disease Predictions
* 📊 Advanced Analytics Dashboard

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Saurabh Kushwaha**
GitHub: https://github.com/Saurabhkushwaha21
