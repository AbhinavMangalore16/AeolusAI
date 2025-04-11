import pandas as pd
import os
from .logger import get_logger
logger = get_logger(__name__)

def append_to_csv(entry: dict, csv_path: str):
    df = pd.DataFrame([entry])

    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_csv(csv_path, index=False)
    logger.info("Appended new weather data to CSV.")
    print("Appended new weather data to CSV.")