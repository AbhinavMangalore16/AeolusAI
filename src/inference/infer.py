import mlflow
import pandas as pd
import requests
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AeolusAI")

# Your OpenWeatherMap API Key
API_KEY = "YOUR_API_KEY_HERE"  # <-- Replace with your real key
CITY = "Delhi"
MODEL_NAME = "TemperatureRegressor"  # or "PrecipitationRegressor"
MODEL_STAGE = "Production"

# Load your ML model
def load_model():
    logger.info(f"📦 Loading model {MODEL_NAME} [{MODEL_STAGE}]")
    return mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")

# Fetch real-time weather data from OpenWeatherMap
def get_realtime_weather():
    logger.info(f"🌤️ Fetching weather for {CITY}")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Extract features matching your model
    weather_features = {
        "humidity": [data["main"]["humidity"]],
        "pressure": [data["main"]["pressure"]],
        "wind_speed": [data["wind"]["speed"]],
        "cloud_coverage": [data["clouds"]["all"]],
        "dew_point": [data["main"]["temp"] - ((100 - data["main"]["humidity"]) / 5)]  # Approximation
        # Add other features if your model uses them
    }

    df = pd.DataFrame(weather_features)
    logger.info(f"📊 Input Data:\n{df}")
    return df

# Run end-to-end inference
def run_inference():
    model = load_model()
    input_df = get_realtime_weather()
    prediction = model.predict(input_df)

    logger.info(f"🎯 Prediction: {prediction[0]:.2f}")
    print(f"\n🔮 Forecasted Value: {prediction[0]:.2f}")
    return prediction[0]

if __name__ == "__main__":
    run_inference()