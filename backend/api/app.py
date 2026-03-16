"""
Flask API application for AI Emotion Monitor.

This module initializes the Flask application, configures CORS,
registers blueprints for API routes, and loads the emotion inference engine.
"""

from flask import Flask, jsonify, current_app
from flask_cors import CORS

from backend.utils.config import config
from backend.core.inference import EmotionInferenceEngine, CalibrationSettings

# Import route blueprints
from backend.api.routes import emotion, session, analytics


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)

    # ===  CORS Configuration ===
    CORS(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # === Load Emotion Inference Engine ===
    try:
        print("Loading emotion inference engine...")
        config.display()  # Display configuration for debugging

        inference_engine = EmotionInferenceEngine(
            model_path=config.MODEL_PATH,
            device=config.DEVICE,
            enable_smoothing=config.ENABLE_SMOOTHING,
            smoothing_window=config.SMOOTHING_WINDOW,
            enable_calibration=config.ENABLE_CALIBRATION,
            calibration_settings=CalibrationSettings(
                sad_boost=config.DEFAULT_SAD_BOOST,
                anger_boost=config.DEFAULT_ANGER_BOOST,
                neutral_suppress=config.DEFAULT_NEUTRAL_SUPPRESS
            )
        )
        app.extensions['inference_engine'] = inference_engine
        print("✓ Emotion inference engine loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load emotion inference engine: {e}")
        raise

    # === Register Blueprints ===
    app.register_blueprint(emotion.bp, url_prefix='/api/emotion')
    app.register_blueprint(session.bp, url_prefix='/api/session')
    app.register_blueprint(analytics.bp, url_prefix='/api/analytics')

    # === Health Check Endpoint ===
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'version': '1.0.0',
            'model_loaded': app.extensions.get('inference_engine') is not None,
            'device': config.DEVICE
        })

    # === Error Handlers ===
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app


def get_inference_engine() -> EmotionInferenceEngine:
    """
    Get the global inference engine instance.

    Returns:
        EmotionInferenceEngine: Global inference engine

    Raises:
        RuntimeError: If inference engine is not initialized
    """
    inference_engine = current_app.extensions.get('inference_engine')
    if inference_engine is None:
        raise RuntimeError("Inference engine not initialized")
    return inference_engine


# === Main Entry Point ===
if __name__ == '__main__':
    app = create_app()
    app.run(
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.API_DEBUG
    )
