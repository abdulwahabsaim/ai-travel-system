from flask import Blueprint, request, jsonify
import logging
from ai_modules.itinerary_generator import ItineraryGenerator

itinerary_bp = Blueprint('itinerary_bp', __name__)
logger = logging.getLogger(__name__)
itinerary_generator = ItineraryGenerator()

@itinerary_bp.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.get_json()
        itinerary = itinerary_generator.generate(
            destination=data.get('destination'),
            start_date=data.get('startDate'),
            end_date=data.get('endDate'),
            budget=data.get('budget'),
            travel_style=data.get('travelStyle', 'balanced'),
            interests=data.get('interests', []),
            group_size=data.get('groupSize', 1)
        )
        return jsonify({'success': True, 'itinerary': itinerary})
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        return jsonify({'error': 'Failed to generate itinerary'}), 500

@itinerary_bp.route('/generate-travel-tips', methods=['POST'])
def generate_travel_tips():
    try:
        data = request.get_json()
        travel_tips = itinerary_generator.generate_travel_tips(
            destination=data.get('destination'),
            travel_style=data.get('travelStyle'),
            interests=data.get('interests', []),
            experience_level=data.get('experienceLevel', 'intermediate')
        )
        return jsonify({'success': True, 'travelTips': travel_tips})
    except Exception as e:
        logger.error(f"Error generating travel tips: {str(e)}")
        return jsonify({'error': 'Failed to generate travel tips'}), 500