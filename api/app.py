import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


MODEL_PATH = "model/anomaly_model.joblib"
FEATURE_COLUMNS = ["temperature", "humidity", "sound_volume"]


app = FastAPI(
    title="IoT Anomaly Detection API",
    description="REST API for detecting anomalies in simulated IoT sensor data.",
    version="1.0.0",
)


class SensorMeasurement(BaseModel):
    temperature: float
    humidity: float
    sound_volume: float


model = joblib.load(MODEL_PATH)


@app.get("/")
def root() -> dict:
    return {
        "message": "IoT Anomaly Detection API is running."
    }


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict")
def predict(measurement: SensorMeasurement) -> dict:
    input_data = pd.DataFrame([{
        "temperature": measurement.temperature,
        "humidity": measurement.humidity,
        "sound_volume": measurement.sound_volume,
    }])

    model_prediction = model.predict(input_data)[0]
    anomaly_score = -model.decision_function(input_data)[0]

    predicted_anomaly = bool(model_prediction == -1)

    return {
        "predicted_anomaly": predicted_anomaly,
        "anomaly_score": round(float(anomaly_score), 4),
        "input": measurement.model_dump()
    }