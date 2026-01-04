"""
Flask ML Application Template
Generated from: KalyanM45/AI-Project-Gallery Analysis
Purpose: Serve trained ML models via REST API

Customization Points:
- Replace MODEL_PATH with actual model location
- Update feature_names, feature_types based on your model
- Add authentication if needed
- Extend prediction endpoint for your use case
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
MODEL_PATH = os.getenv('MODEL_PATH', 'Artifacts/model.pkl')
PREPROCESSOR_PATH = os.getenv('PREPROCESSOR_PATH', 'Artifacts/preprocessor.pkl')
METADATA_PATH = os.getenv('METADATA_PATH', 'Artifacts/model_metadata.json')

# Global model and preprocessor (loaded on startup)
model = None
preprocessor = None
model_metadata = None


def load_model():
    """Load model, preprocessor, and metadata at startup."""
    global model, preprocessor, model_metadata

    try:
        model = joblib.load(MODEL_PATH)
        logger.info(f"Model loaded from {MODEL_PATH}")
    except FileNotFoundError:
        logger.error(f"Model file not found at {MODEL_PATH}")
        raise

    try:
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        logger.info(f"Preprocessor loaded from {PREPROCESSOR_PATH}")
    except FileNotFoundError:
        logger.warning(f"Preprocessor not found at {PREPROCESSOR_PATH}")
        preprocessor = None

    try:
        with open(METADATA_PATH, 'r') as f:
            model_metadata = json.load(f)
        logger.info(f"Metadata loaded from {METADATA_PATH}")
    except FileNotFoundError:
        logger.warning(f"Metadata not found at {METADATA_PATH}")
        model_metadata = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model_loaded': model is not None
    })


@app.route('/model-info', methods=['GET'])
def model_info():
    """Return model metadata and capabilities."""
    if model_metadata is None:
        return jsonify({'error': 'Model metadata not available'}), 500

    return jsonify({
        'model_type': model_metadata.get('model_type', 'Unknown'),
        'training_date': model_metadata.get('training_date', 'Unknown'),
        'features': model_metadata.get('features', []),
        'metrics': model_metadata.get('metrics', {}),
        'constraints': model_metadata.get('constraints', []),
        'known_limitations': model_metadata.get('known_limitations', [])
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make predictions on input data.

    Expected JSON input:
    {
        "features": [feature1, feature2, ...] OR
        "data": {"col1": value1, "col2": value2, ...}
    }

    Returns:
    {
        "prediction": value,
        "confidence": confidence_score (if applicable),
        "timestamp": ISO timestamp,
        "model_version": model version info
    }
    """
    try:
        # Parse request
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Handle two input formats
        if 'features' in data:
            # List of feature values
            features = np.array(data['features']).reshape(1, -1)
            logger.info(f"Features input shape: {features.shape}")
        elif 'data' in data:
            # Dictionary of feature names -> values
            df = pd.DataFrame([data['data']])
            features = df.values
            logger.info(f"DataFrame input shape: {features.shape}")
        else:
            return jsonify({'error': 'Input must contain "features" or "data"'}), 400

        # Preprocess if preprocessor exists
        if preprocessor is not None:
            try:
                features = preprocessor.transform(features)
                logger.info("Features preprocessed successfully")
            except Exception as e:
                logger.error(f"Preprocessing failed: {e}")
                return jsonify({'error': f'Preprocessing failed: {str(e)}'}), 500

        # Make prediction
        try:
            prediction = model.predict(features)[0]

            # Try to get prediction probability for classification models
            confidence = None
            try:
                if hasattr(model, 'predict_proba'):
                    proba = model.predict_proba(features)[0]
                    confidence = float(np.max(proba))
            except:
                pass

            logger.info(f"Prediction: {prediction}, Confidence: {confidence}")

            # Format response
            response = {
                'prediction': float(prediction) if isinstance(prediction, (np.integer, np.floating)) else prediction,
                'timestamp': datetime.utcnow().isoformat(),
                'model_type': model_metadata.get('model_type', 'Unknown')
            }

            if confidence is not None:
                response['confidence'] = confidence

            return jsonify(response)

        except Exception as e:
            logger.error(f"Prediction failed: {e}", exc_info=True)
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON'}), 400
    except Exception as e:
        logger.error(f"Unexpected error in /predict: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Make predictions on multiple samples.

    Expected JSON input:
    {
        "data": [
            {"col1": val1, "col2": val2},
            {"col1": val3, "col2": val4}
        ]
    }

    Returns:
    {
        "predictions": [pred1, pred2, ...],
        "count": number_of_predictions,
        "timestamp": ISO timestamp
    }
    """
    try:
        data = request.get_json()

        if not data or 'data' not in data:
            return jsonify({'error': 'Input must contain "data" array'}), 400

        # Convert to DataFrame
        df = pd.DataFrame(data['data'])
        features = df.values

        # Preprocess if preprocessor exists
        if preprocessor is not None:
            features = preprocessor.transform(features)

        # Make predictions
        predictions = model.predict(features)

        response = {
            'predictions': [float(p) if isinstance(p, (np.integer, np.floating)) else p for p in predictions],
            'count': len(predictions),
            'timestamp': datetime.utcnow().isoformat()
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Batch prediction failed: {e}", exc_info=True)
        return jsonify({'error': f'Batch prediction failed: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Load model on startup
    load_model()

    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting Flask app on {host}:{port} (debug={debug})")

    # Run Flask app
    app.run(host=host, port=port, debug=debug)
