# train_temp_model.py

import mlflow
import mlflow.sklearn
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import logging
import joblib
from models import get_model_dict
from data import load_temperature_data  # <- This should load X_train_temp, X_test_temp, etc.

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AeolusAI")

mlflow.set_experiment("temperature_regression")

def train_and_log_temperature_models():
    X_train, X_test, y_train, y_test = load_temperature_data()
    y_train = y_train.ravel()
    y_test = y_test.ravel()
    models = get_model_dict()

    best_model = None
    best_score = -np.inf
    best_name = ""
    best_run_id = ""

    for name, model in models.items():
        try:
            with mlflow.start_run(run_name=f"{name}_temp") as run:
                logger.info(f"🌡️ Training {name} for temperature regression...")

                cv_mae = -cross_val_score(model, X_train, y_train, cv=2, scoring="neg_mean_absolute_error").mean()
                cv_r2 = cross_val_score(model, X_train, y_train, cv=2, scoring="r2").mean()

                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                mae = mean_absolute_error(y_test, y_pred)
                rmse = mean_squared_error(y_test, y_pred, squared=False)
                r2 = r2_score(y_test, y_pred)

                logger.info(f"📊 {name} | MAE: {mae:.3f}, RMSE: {rmse:.3f}, R2: {r2:.3f}")

                mlflow.set_tags({"developer": "Abhinav", "stage": "dev"})
                mlflow.log_param("model_name", name)
                mlflow.log_metrics({
                    "cv_mae": cv_mae,
                    "cv_r2": cv_r2,
                    "test_mae": mae,
                    "test_rmse": rmse,
                    "test_r2": r2
                })

                mlflow.sklearn.log_model(model, "model")

                if r2 > best_score:
                    best_score = r2
                    best_model = model
                    best_name = name
                    best_run_id = run.info.run_id

        except Exception as e:
            logger.error(f"❌ Error training {name}: {e}")

    if best_model:
        logger.info(f"🏅 Best temperature model: {best_name} | R2: {best_score:.3f}")
        model_uri = f"runs:/{best_run_id}/model"
        result = mlflow.register_model(model_uri=model_uri, name="TemperatureRegressor")
        joblib.dump(best_model, "best_temp_model.pkl")
        logger.info(f"✅ Registered model version: {result.version}")

if __name__ == "__main__":
    train_and_log_temperature_models()
