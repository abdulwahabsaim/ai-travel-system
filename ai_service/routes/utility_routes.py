from flask import Blueprint, request, jsonify
import logging
from ai_modules.sentiment_analyzer import SentimentAnalyzer
from ai_modules.weather_analyzer import WeatherAnalyzer
from ai_modules.translation_service import TranslationService

utility_bp = Blueprint('utility_bp', __name__)
logger = logging.getLogger(__name__)

sentiment_analyzer = SentimentAnalyzer()
weather_analyzer = WeatherAnalyzer()
translation_service = TranslationService()

@utility_bp.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        sentiment_result = sentiment_analyzer.analyze(data.get('text'))
        return jsonify({'success': True, 'sentiment': sentiment_result})
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return jsonify({'error': 'Failed to analyze sentiment'}), 500

@utility_bp.route('/get-weather-insights', methods=['POST'])
def get_weather_insights():
    try:
        data = request.get_json()
        weather_insights = weather_analyzer.get_insights(
            destination=data.get('destination'),
            travel_dates=data.get('travelDates')
        )
        return jsonify({'success': True, 'weatherInsights': weather_insights})
    except Exception as e:
        logger.error(f"Error getting weather insights: {str(e)}")
        return jsonify({'error': 'Failed to get weather insights'}), 500

@utility_bp.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        translation = translation_service.translate(
            text=data.get('text'),
            target_language=data.get('targetLanguage'),
            source_language=data.get('sourceLanguage', 'auto')
        )
        return jsonify({'success': True, 'translation': translation})
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return jsonify({'error': 'Failed to translate text'}), 500