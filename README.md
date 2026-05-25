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

The `contamination` parameter was set to `0.11`. During testing, a value of `0.10` resulted in one missed simulated anomaly. Since missing a real anomaly in a manufacturing environment could lead to faulty products, machine downtime, or quality issues, the model was adjusted to be slightly more sensitive.

With `contamination = 0.11`, the model accepted a small number of false positives but avoided false negatives in the tested training run. This trade-off is appropriate for the use case because a false alarm only triggers an additional inspection, while a missed anomaly could have more serious consequences.


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

## Status

Core local pipeline implemented: data simulation, model training, REST API, streaming simulation, prediction logging, and monitoring summary.