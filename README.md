# PhishLens

End-to-end machine learning pipeline for phishing URL detection.

## Architecture

- **Data Pipeline**: Ingestion → Validation → Transformation → Training
- **Models**: XGBoost, Logistic Regression, GaussianNB with hyperparameter tuning
- **API**: Flask REST service with CSV upload/download workflow
- **Database**: MongoDB for data persistence
- **Deployment**: Dockerized application on Render

## Project Structure

```
src/
├── components/       # ML pipeline components
├── configuration/    # MongoDB connection
├── data_access/      # Data retrieval
├── pipeline/         # Training and prediction pipelines
├── utils/            # Utilities
├── logger.py         # Logging configuration
├── exception.py      # Custom exceptions

config/
├── model.yaml        # Model hyperparameters
├── training_schema.json  # Data validation schema
```

## Requirements

See `requirements.txt` for dependencies.

## Environment Configuration

Required environment variables (`.env`):
```
MONGO_DB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
FLASK_ENV=production
FLASK_DEBUG=False
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status |
| `/health` | GET | Health check |
| `/predict` | GET | Prediction interface |
| `/predict` | POST | Batch prediction (CSV upload) |
| `/train` | POST | Model training |

## Deployment

Docker container configured with Gunicorn WSGI server. Deploy on Render with `render.yaml` configuration.
