import argparse
import csv
import os
import time

import requests

from data.sensor_generator import generate_sensor_data


API_URL = "http://127.0.0.1:8000/predict"

LOG_FILE_PATH = "monitoring/prediction_log.csv"

LOG_FIELDNAMES = [
    "timestamp",
    "temperature",
    "humidity",
    "sound_volume",
    "is_simulated_anomaly",
    "predicted_anomaly",
    "anomaly_score",
]


def send_measurement_to_api(measurement: dict) -> dict:
    """Send one sensor measurement to the prediction API."""
    payload = {
        "temperature": measurement["temperature"],
        "humidity": measurement["humidity"],
        "sound_volume": measurement["sound_volume"],
    }

    response = requests.post(API_URL, json=payload, timeout=5)
    response.raise_for_status()

    return response.json()


def log_prediction(measurement: dict, prediction: dict) -> None:
    """Append one sensor measurement and its prediction to a CSV log file."""
    file_exists = os.path.exists(LOG_FILE_PATH)

    row = {
        "timestamp": measurement["timestamp"],
        "temperature": measurement["temperature"],
        "humidity": measurement["humidity"],
        "sound_volume": measurement["sound_volume"],
        "is_simulated_anomaly": measurement["is_simulated_anomaly"],
        "predicted_anomaly": prediction["predicted_anomaly"],
        "anomaly_score": prediction["anomaly_score"],
    }

    with open(LOG_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=LOG_FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


def run_sensor_stream(interval_seconds: int = 2, anomaly_probability: float = 0.1) -> None:
    """Continuously generate sensor data and send it to the API."""
    print("Starting simulated sensor stream...")
    print("Press Ctrl+C to stop.")
    print(f"Interval seconds: {interval_seconds}")
    print(f"Anomaly probability: {anomaly_probability}")
    print()

    while True:
        measurement = generate_sensor_data(anomaly_probability=anomaly_probability)
        prediction = send_measurement_to_api(measurement)
        log_prediction(measurement, prediction)

        print("New sensor measurement:")
        print(f"  Temperature: {measurement['temperature']} °C")
        print(f"  Humidity: {measurement['humidity']} %")
        print(f"  Sound volume: {measurement['sound_volume']} dB")
        print(f"  Simulated anomaly: {measurement['is_simulated_anomaly']}")
        print(f"  Predicted anomaly: {prediction['predicted_anomaly']}")
        print(f"  Anomaly score: {prediction['anomaly_score']}")
        print("-" * 50)

        time.sleep(interval_seconds)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the sensor stream."""
    parser = argparse.ArgumentParser(
        description="Simulate a continuous IoT sensor stream and send measurements to the prediction API."
    )

    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=2,
        help="Time interval in seconds between two sensor measurements.",
    )

    parser.add_argument(
        "--anomaly-probability",
        type=float,
        default=0.1,
        help="Probability of generating an anomalous sensor measurement.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    try:
        run_sensor_stream(
            interval_seconds=args.interval_seconds,
            anomaly_probability=args.anomaly_probability,
        )
    except KeyboardInterrupt:
        print("\nSensor stream stopped by user.")