from data.fetch_weather import get_weather_data
from utils.utils import append_to_csv
from utils.logger import get_logger
import schedule
import time

logger = get_logger("weather_fetcher")
CSV_PATH = "data/raw/training_data1.csv"

def job():
    try:
        data = get_weather_data("Delhi")
        append_to_csv(data, CSV_PATH)
        logger.info(f"Logged data: {data}")
    except Exception as e:
        logger.exception("Weather fetch failed")

schedule.every(5).minutes.do(job)

logger.info("Weather fetcher started.")
job()  # first run
while True:
    schedule.run_pending()
    time.sleep(1)
