from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.logger import logging as lg
import os, sys
from dotenv import load_dotenv

from src.pipeline.train_pipeline import TrainingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

# Load environment variables
load_dotenv()

# Validate required environment variables
required_env_vars = ['MONGO_DB_URL']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "success", "message": "PhishLens API is running"})

@app.route("/health")
def health():
    if missing_vars:
        return jsonify({
            "status": "unhealthy",
            "message": f"Missing environment variables: {', '.join(missing_vars)}"
        }), 503
    return jsonify({"status": "healthy"}), 200

@app.route("/train", methods=['POST', 'GET'])
def train_route():
    try:
        if missing_vars:
            return jsonify({
                "status": "error",
                "message": f"Cannot start training: Missing environment variables: {', '.join(missing_vars)}"
            }), 503
            
        lg.info("=== TRAINING STARTED ===")
        train_pipeline = TrainingPipeline()
        lg.info("Training pipeline created")
        
        train_pipeline.run_pipeline()
        lg.info("Training pipeline completed successfully")
        
        return jsonify({"status": "success", "message": "Training Completed."}), 200

    except Exception as e:
        error_msg = str(e)
        lg.error(f"Training failed: {error_msg}", exc_info=True)
        return jsonify({"status": "error", "message": error_msg}), 500

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        if missing_vars:
            return jsonify({
                "status": "error",
                "message": f"Cannot make predictions: Missing environment variables: {', '.join(missing_vars)}"
            }), 503
            
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_detail = prediction_pipeline.run_pipeline()

            lg.info("Prediction completed. Downloading prediction file.")
            return send_file(prediction_file_detail.prediction_file_path,
                            download_name=prediction_file_detail.prediction_file_name,
                            as_attachment=True)
        
        else:
            return render_template('prediction.html')

    except Exception as e:
        lg.error(f"Prediction failed: {str(e)}")
        raise CustomException(e, sys)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    error_msg = str(error)
    import traceback
    error_traceback = traceback.format_exc()
    lg.error(f"500 Error: {error_msg}\n{error_traceback}")
    return jsonify({
        "status": "error", 
        "message": error_msg or "Internal server error",
        "traceback": error_traceback if os.getenv("FLASK_ENV") == "development" else None
    }), 500

if __name__ == "__main__":
    # In production, gunicorn will handle the server
    # This is only for development
    debug_mode = os.getenv("FLASK_ENV", "production") == "development"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)