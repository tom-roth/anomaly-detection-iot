import pandas as pd


LOG_FILE_PATH = "monitoring/prediction_log.csv"


def load_prediction_log(path: str = LOG_FILE_PATH) -> pd.DataFrame:
    """Load the prediction log from a CSV file."""
    return pd.read_csv(path)


def analyze_predictions(data: pd.DataFrame) -> None:
    """Print a simple monitoring summary for logged predictions."""
    total_measurements = len(data)
    predicted_anomalies = data["predicted_anomaly"].sum()
    simulated_anomalies = data["is_simulated_anomaly"].sum()

    average_score = data["anomaly_score"].mean()
    max_score = data["anomaly_score"].max()

    latest_measurement = data.iloc[-1]

    print("Prediction Monitoring Summary")
    print("-" * 40)
    print(f"Total measurements: {total_measurements}")
    print(f"Predicted anomalies: {predicted_anomalies}")
    print(f"Simulated anomalies: {simulated_anomalies}")
    print(f"Average anomaly score: {average_score:.4f}")
    print(f"Highest anomaly score: {max_score:.4f}")

    print("\nLatest measurement:")
    print(f"Timestamp: {latest_measurement['timestamp']}")
    print(f"Temperature: {latest_measurement['temperature']} °C")
    print(f"Humidity: {latest_measurement['humidity']} %")
    print(f"Sound volume: {latest_measurement['sound_volume']} dB")
    print(f"Predicted anomaly: {latest_measurement['predicted_anomaly']}")
    print(f"Anomaly score: {latest_measurement['anomaly_score']}")


if __name__ == "__main__":
    prediction_log = load_prediction_log()
    analyze_predictions(prediction_log)