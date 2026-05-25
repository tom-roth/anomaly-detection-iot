import pandas as pd

from data.sensor_generator import generate_sensor_data


def create_training_data(number_of_rows: int = 1000) -> pd.DataFrame:
    """Create a training dataset with simulated IoT sensor data."""
    sensor_data = []

    for _ in range(number_of_rows):
        measurement = generate_sensor_data(anomaly_probability=0.1)
        sensor_data.append(measurement)

    return pd.DataFrame(sensor_data)


if __name__ == "__main__":
    df = create_training_data(number_of_rows=1000)

    output_path = "data/training_sensor_data.csv"
    df.to_csv(output_path, index=False)

    print(f"Training data created: {output_path}")
    print(df.head())
    print("\nDataset shape:", df.shape)
    print("\nAnomaly distribution:")
    print(df["is_simulated_anomaly"].value_counts())