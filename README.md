# AeolusAI - Weather Forecast & Precipitation Prediction Dashboard

## 🌤️ Overview
A sleek weather dashboard that combines real-time forecast data and a trained ML model (for precipitation prediction) to deliver 5-day weather insights.

## ⚙️ Key Features
- Real-time weather forecast using OpenWeatherMap API
- ML-based precipitation prediction pipeline (logged using MLflow)
- Responsive and clean dashboard UI
- Model performance tracked and registered with MLflow

## 🧠 Tech Stack
- Frontend: React + Tailwind
- Backend (DS): Random Forest, XGBoost, GBRT (via scikit-learn), MLflow, Python
- Data Source: OpenWeatherMap API
- Deployment: Vercel, Cron(https://aeolus-ai.vercel.app/)

## 🔍 ML Approach
- Model: Regression for precipitation
- Trained on historical weather data
- MAE/RMSE/R² logged via MLflow
- Code and metrics available in [link to Google Drive if needed]

## 📦 How to Run
1. Clone the repo
2. Add a `.env` file with:
VITE_API_KEY=your_openweathermap_api_key
3. Run the app:
```bash
python -m venv venv
pip install -r requirements.txt
cd frontend
npm install
npm run dev
```

## Data, Model and Experiment Tracking Folder:
Drive link: https://drive.google.com/drive/folders/18DQYmg1kVqzTMWhU-ePrN46kgn_JWazn?usp=drive_link
