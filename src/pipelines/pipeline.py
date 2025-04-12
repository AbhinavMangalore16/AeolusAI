import logging
from data import load_csv, save_parquet
from features import create_features
from models import train_model, train_model_temp
from inference import run_inference
from sklearn.model_selection import train_test_split
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AeolusAI-Pipeline")

def main():
    csv_path = "data/raw/weather.csv"
    parquet_path = "data/processed/weather.parquet"
    pipeline_path = "models/feature_pipeline.joblib"
    api_key = os.environ.get("OPEN_WEATHER_API_KEY")
    city = "Delhi"

    df = load_csv(csv_path)
    save_parquet(df, parquet_path)

    import pandas as pd
    df = pd.read_parquet(parquet_path)
    X, y = create_features(df, save_path=pipeline_path)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    train_and_log_models()
    train_and_log_temperature_models()

    prediction = run_inference(api_key, city)
    print(f"🌤️ Final predicted weather metric: {prediction:.2f}")

if __name__ == "__main__":
    main()
