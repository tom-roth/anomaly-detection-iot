import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix


DATA_PATH = "data/training_sensor_data.csv"
MODEL_PATH = "model/anomaly_model.joblib"

FEATURE_COLUMNS = ["temperature", "humidity", "sound_volume"]


def load_training_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load the simulated sensor training data from a CSV file."""
    return pd.read_csv(path)


def train_anomaly_model(data: pd.DataFrame) -> IsolationForest:
    """Train a simple Isolation Forest model for anomaly detection."""
    features = data[FEATURE_COLUMNS]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.11,
        random_state=42,
    )

    model.fit(features)

    return model


def evaluate_model(model: IsolationForest, data: pd.DataFrame) -> pd.DataFrame:
    """Add anomaly predictions and anomaly scores to the dataset."""
    result = data.copy()
    features = result[FEATURE_COLUMNS]

    result["model_prediction"] = model.predict(features)
    result["anomaly_score"] = -model.decision_function(features)

    result["predicted_anomaly"] = result["model_prediction"].map({
        1: False,
        -1: True,
    })

    return result


def save_model(model: IsolationForest, path: str = MODEL_PATH) -> None:
    """Save the trained model to disk."""
    joblib.dump(model, path)


def print_evaluation_metrics(result: pd.DataFrame) -> None:
    """Print basic evaluation metrics based on simulated anomaly labels."""
    y_true = result["is_simulated_anomaly"]
    y_pred = result["predicted_anomaly"]

    print("\nConfusion matrix:")
    print(confusion_matrix(y_true, y_pred))

    print("\nClassification report:")
    print(classification_report(y_true, y_pred))


if __name__ == "__main__":
    df = load_training_data()
    model = train_anomaly_model(df)
    result_df = evaluate_model(model, df)
    print_evaluation_metrics(result_df)

    save_model(model)

    print("Model training completed.")
    print(f"Model saved to: {MODEL_PATH}")

    print("\nDataset shape:")
    print(result_df.shape)

    print("\nPrediction distribution:")
    print(result_df["predicted_anomaly"].value_counts())

    print("\nAverage anomaly score:")
    print(result_df["anomaly_score"].mean())

    print("\nSample predictions:")
    print(result_df.head())