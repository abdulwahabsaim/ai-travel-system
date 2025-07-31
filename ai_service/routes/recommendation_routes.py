from flask import Blueprint, request, jsonify
import logging
from ai_modules.recommendation_engine import RecommendationEngine

recommendation_bp = Blueprint('recommendation_bp', __name__)
logger = logging.getLogger(__name__)
recommendation_engine = RecommendationEngine()

@recommendation_bp.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        recommendations = recommendation_engine.get_recommendations(
            user_preferences=data.get('preferences', {}),
            budget_range=data.get('budgetRange'),
            travel_history=data.get('travelHistory', []),
            interests=data.get('interests', [])
        )
        return jsonify({'success': True, 'recommendations': recommendations})
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({'error': 'Failed to get recommendations'}), 500