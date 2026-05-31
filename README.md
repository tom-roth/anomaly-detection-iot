# Anomaly Detection for IoT Sensor Data

This project implements a local end-to-end anomaly detection system for simulated IoT sensor data in a manufacturing environment.

The scenario is based on a modern factory producing machine components for wind turbines. Sensors continuously measure temperature, humidity, and sound volume during the production cycle. A machine learning model predicts an anomaly score for each incoming sensor measurement and exposes the prediction through a RESTful API.

## Project Goals

- Simulate continuous IoT sensor data
- Train a simple anomaly detection model in Python
- Serve the model through a RESTful API
- Process simulated sensor streams
- Log predictions for monitoring purposes
- Provide a reproducible project structure for presentation and portfolio use

## Planned Architecture

```text
Sensor Simulation
        ↓
REST API
        ↓
Anomaly Detection Model
        ↓
Prediction Response
        ↓
Logging / Monitoring
```

For a detailed architecture diagram, see [System Architecture](docs/system_architecture.md).

## Tech Stack

- Python
- FastAPI
- scikit-learn
- pandas
- NumPy
- joblib
- requests
- matplotlib

## Project Structure

```text
anomaly-detection-iot/
├── api/
├── data/
├── model/
├── monitoring/
├── notebooks/
├── tests/
├── docs/
├── README.md
├── requirements.txt
└── .gitignore
```

## Model Choice and Configuration

The anomaly detection model is based on an Isolation Forest. This model was chosen because it is suitable for detecting unusual patterns in numerical sensor data and does not require a highly complex supervised learning setup.

The model uses the following input features:

- temperature
- humidity
- sound_volume

The `contamination` parameter was set to `0.11`. During one evaluation run, a value of `0.10` resulted in one missed simulated anomaly. Since missing a real anomaly in a manufacturing environment could lead to faulty products, machine downtime, or quality issues, the model was adjusted to be slightly more sensitive.

With `contamination = 0.11`, the model accepted a small number of false positives but avoided false negatives in the tested training run. This trade-off is appropriate for the use case because a false alarm only triggers an additional inspection, while a missed anomaly could have more serious consequences.


## Setup

Clone the repository and navigate into the project folder:

```bash
git clone https://github.com/tom-roth/anomaly-detection-iot.git
cd anomaly-detection-iot
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```


## How to Run the Project

### 1. Create training data

```bash
python -m data.create_training_data
```

### 2. Train the model

```bash
python -m model.train_model
```

### 3. Start the API

```bash
uvicorn api.app:app --reload
```

### 4. Open API documentation

```text
http://127.0.0.1:8000/docs
```

### 5. Start the simulated sensor stream

```bash
python -m data.sensor_stream
```

Demo mode with more anomalies and faster streaming:

```bash
python -m data.sensor_stream --anomaly-probability 0.3 --interval-seconds 1
```

### 6. Analyze logged predictions

```bash
python -m monitoring.analyze_predictions
```

## Example API Request

After starting the FastAPI server, predictions can be requested via the `POST /predict` endpoint.

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{"temperature": 120, "humidity": 90, "sound_volume": 115}'
```

Example response:

```json
{
  "predicted_anomaly": true,
  "anomaly_score": 0.0872,
  "input": {
    "temperature": 120.0,
    "humidity": 90.0,
    "sound_volume": 115.0
  }
}
```

A higher anomaly score indicates a more unusual sensor pattern.


## Monitoring

The sensor stream logs each prediction to `monitoring/prediction_log.csv`. Each log entry contains the timestamp, input sensor values, simulated anomaly label, predicted anomaly flag, and anomaly score.

The monitoring summary can be generated with:

```bash
python -m monitoring.analyze_predictions
```

Example output:

```text
Prediction Monitoring Summary
----------------------------------------
Total measurements: 81
Predicted anomalies: 16
Simulated anomalies: 16
Average anomaly score: -0.0413
Highest anomaly score: 0.1593
```

This lightweight monitoring approach makes the model behavior observable over time and helps identify when anomalies occur during simulated operation.


## Limitations

This project is a local prototype and does not represent a fully deployed production system.

Current limitations include:

- Sensor data is simulated and not collected from real industrial machines.
- The model is trained on fictional data, so its performance does not represent real-world production accuracy.
- The REST API runs locally and is not deployed to cloud infrastructure.
- Monitoring is implemented as lightweight CSV-based logging and summary analysis.
- Model retraining is manual and not automated through a full MLOps pipeline.

These limitations are acceptable for the scope of this project because the main goal is to demonstrate the integration of a predictive model into a production-like service architecture.


## Future Improvements

Possible future improvements include:

- Deploying the REST API in a cloud environment or containerizing it with Docker.
- Replacing simulated sensor data with real IoT sensor data from a production system.
- Adding automated model retraining when new data becomes available.
- Using a message broker such as Kafka or MQTT for more realistic stream processing.
- Extending monitoring with dashboards, alerting, and data drift detection.
- Adding automated tests for the API and model pipeline.
- Storing prediction logs in a database instead of a local CSV file.

These improvements would make the system more robust, scalable, and closer to a real production environment.


## Status

Core local pipeline implemented: data simulation, model training, REST API, streaming simulation, prediction logging, and monitoring summary.