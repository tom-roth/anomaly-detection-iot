# System Architecture

This document describes the conceptual architecture of the anomaly detection system.

The architecture consists of two main flows:

- Training Flow
- Serving / Stream Flow

```mermaid
flowchart LR
    subgraph TrainingFlow["Training Flow"]
        A["Simulated Training Data<br/>training_sensor_data.csv"] --> B["Model Training<br/>train_model.py"]
        B --> C["Model Evaluation<br/>Confusion Matrix & Classification Report"]
        C --> D["Saved Model Artifact<br/>anomaly_model.joblib"]
    end

    subgraph ServingFlow["Serving / Stream Flow"]
        E["Simulated IoT Sensors<br/>temperature, humidity, sound_volume"] --> F["Sensor Stream Application<br/>sensor_stream.py"]
        F --> G["FastAPI REST API<br/>POST /predict"]
        G --> H["Loaded Anomaly Detection Model"]
        H --> I["Prediction Response<br/>predicted_anomaly + anomaly_score"]
        I --> J["Prediction Log CSV<br/>prediction_log.csv"]
        J --> K["Monitoring Summary<br/>analyze_predictions.py"]
    end

    D --> H
```

## Explanation

The training flow prepares the anomaly detection model. Simulated sensor data is generated and stored as a CSV file. The model training script trains an Isolation Forest model, evaluates it with basic metrics, and saves the trained model as a reusable model artifact.

The serving flow uses the saved model in a production-like setup. A simulated sensor stream continuously generates new measurements and sends them to a REST API. The API loads the saved model and returns a prediction response containing an anomaly flag and an anomaly score. Each prediction is logged to a CSV file and can be analyzed through a lightweight monitoring summary.