from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
import logging

# Import Blueprints
from routes.main_routes import main_bp
from routes.itinerary_routes import itinerary_bp
from routes.cost_routes import cost_bp
from routes.recommendation_routes import recommendation_bp
from routes.utility_routes import utility_bp

# Load environment variables from .env file in the ai_service directory
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(itinerary_bp)
app.register_blueprint(cost_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(utility_bp)


if __name__ == '__main__':
    # Use the PORT from the .env file in this directory, defaulting to 5001
    port = int(os.environ.get('PORT', 5001))
    # Use 0.0.0.0 to make it accessible on your network
    app.run(host='0.0.0.0', port=port, debug=True)