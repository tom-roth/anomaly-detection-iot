import random
from datetime import datetime, UTC


def generate_normal_sensor_data() -> dict:
    """Generate one normal sensor measurement."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "temperature": round(random.uniform(70, 90), 2),
        "humidity": round(random.uniform(35, 55), 2),
        "sound_volume": round(random.uniform(60, 80), 2),
    }


def generate_anomalous_sensor_data() -> dict:
    """Generate one anomalous sensor measurement."""
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "temperature": round(random.uniform(100, 130), 2),
        "humidity": round(random.uniform(70, 95), 2),
        "sound_volume": round(random.uniform(95, 130), 2),
    }


def generate_sensor_data(anomaly_probability: float = 0.1) -> dict:
    """
    Generate one sensor measurement.

    With a configurable probability, the measurement is anomalous.
    """
    if random.random() < anomaly_probability:
        data = generate_anomalous_sensor_data()
        data["is_simulated_anomaly"] = True
    else:
        data = generate_normal_sensor_data()
        data["is_simulated_anomaly"] = False

    return data


if __name__ == "__main__":
    for _ in range(5):
        print(generate_sensor_data())