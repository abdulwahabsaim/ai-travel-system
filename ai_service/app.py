from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime, timedelta
import random

# Import AI modules
from ai_modules.itinerary_generator import ItineraryGenerator
from ai_modules.cost_predictor import CostPredictor
from ai_modules.recommendation_engine import RecommendationEngine
from ai_modules.sentiment_analyzer import SentimentAnalyzer
from ai_modules.weather_analyzer import WeatherAnalyzer
from ai_modules.translation_service import TranslationService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize AI modules
itinerary_generator = ItineraryGenerator()
cost_predictor = CostPredictor()
recommendation_engine = RecommendationEngine()
sentiment_analyzer = SentimentAnalyzer()
weather_analyzer = WeatherAnalyzer()
translation_service = TranslationService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Travel Service',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    """Generate AI-powered travel itinerary"""
    try:
        data = request.get_json()
        
        # Extract parameters
        destination = data.get('destination')
        start_date = data.get('startDate')
        end_date = data.get('endDate')
        budget = data.get('budget')
        travel_style = data.get('travelStyle', 'balanced')
        interests = data.get('interests', [])
        group_size = data.get('groupSize', 1)
        
        if not all([destination, start_date, end_date, budget]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Generate itinerary
        itinerary = itinerary_generator.generate(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            travel_style=travel_style,
            interests=interests,
            group_size=group_size
        )
        
        return jsonify({
            'success': True,
            'itinerary': itinerary
        })
        
    except Exception as e:
        logger.error(f"Error generating itinerary: {str(e)}")
        return jsonify({'error': 'Failed to generate itinerary'}), 500

@app.route('/predict-costs', methods=['POST'])
def predict_costs():
    """Predict travel costs for a destination"""
    try:
        data = request.get_json()
        
        destination = data.get('destination')
        duration = data.get('duration')
        travel_style = data.get('travelStyle', 'balanced')
        group_size = data.get('groupSize', 1)
        season = data.get('season')
        
        if not all([destination, duration]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Predict costs
        cost_prediction = cost_predictor.predict(
            destination=destination,
            duration=duration,
            travel_style=travel_style,
            group_size=group_size,
            season=season
        )
        
        return jsonify({
            'success': True,
            'costPrediction': cost_prediction
        })
        
    except Exception as e:
        logger.error(f"Error predicting costs: {str(e)}")
        return jsonify({'error': 'Failed to predict costs'}), 500

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    """Get personalized travel recommendations"""
    try:
        data = request.get_json()
        
        user_preferences = data.get('preferences', {})
        budget_range = data.get('budgetRange')
        travel_history = data.get('travelHistory', [])
        interests = data.get('interests', [])
        
        # Get recommendations
        recommendations = recommendation_engine.get_recommendations(
            user_preferences=user_preferences,
            budget_range=budget_range,
            travel_history=travel_history,
            interests=interests
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return jsonify({'error': 'Failed to get recommendations'}), 500

@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    """Analyze sentiment of travel reviews"""
    try:
        data = request.get_json()
        
        text = data.get('text')
        if not text:
            return jsonify({'error': 'Missing text parameter'}), 400
        
        # Analyze sentiment
        sentiment_result = sentiment_analyzer.analyze(text)
        
        return jsonify({
            'success': True,
            'sentiment': sentiment_result
        })
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return jsonify({'error': 'Failed to analyze sentiment'}), 500

@app.route('/get-weather-insights', methods=['POST'])
def get_weather_insights():
    """Get weather insights for travel planning"""
    try:
        data = request.get_json()
        
        destination = data.get('destination')
        travel_dates = data.get('travelDates')
        
        if not all([destination, travel_dates]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Get weather insights
        weather_insights = weather_analyzer.get_insights(
            destination=destination,
            travel_dates=travel_dates
        )
        
        return jsonify({
            'success': True,
            'weatherInsights': weather_insights
        })
        
    except Exception as e:
        logger.error(f"Error getting weather insights: {str(e)}")
        return jsonify({'error': 'Failed to get weather insights'}), 500

@app.route('/translate', methods=['POST'])
def translate_text():
    """Translate text for international travel"""
    try:
        data = request.get_json()
        
        text = data.get('text')
        target_language = data.get('targetLanguage')
        source_language = data.get('sourceLanguage', 'auto')
        
        if not all([text, target_language]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Translate text
        translation = translation_service.translate(
            text=text,
            target_language=target_language,
            source_language=source_language
        )
        
        return jsonify({
            'success': True,
            'translation': translation
        })
        
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return jsonify({'error': 'Failed to translate text'}), 500

@app.route('/optimize-budget', methods=['POST'])
def optimize_budget():
    """Optimize travel budget allocation"""
    try:
        data = request.get_json()
        
        total_budget = data.get('totalBudget')
        destination = data.get('destination')
        duration = data.get('duration')
        preferences = data.get('preferences', {})
        
        if not all([total_budget, destination, duration]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Optimize budget
        budget_optimization = cost_predictor.optimize_budget(
            total_budget=total_budget,
            destination=destination,
            duration=duration,
            preferences=preferences
        )
        
        return jsonify({
            'success': True,
            'budgetOptimization': budget_optimization
        })
        
    except Exception as e:
        logger.error(f"Error optimizing budget: {str(e)}")
        return jsonify({'error': 'Failed to optimize budget'}), 500

@app.route('/generate-travel-tips', methods=['POST'])
def generate_travel_tips():
    """Generate personalized travel tips"""
    try:
        data = request.get_json()
        
        destination = data.get('destination')
        travel_style = data.get('travelStyle')
        interests = data.get('interests', [])
        experience_level = data.get('experienceLevel', 'intermediate')
        
        if not destination:
            return jsonify({'error': 'Missing destination parameter'}), 400
        
        # Generate travel tips
        travel_tips = itinerary_generator.generate_travel_tips(
            destination=destination,
            travel_style=travel_style,
            interests=interests,
            experience_level=experience_level
        )
        
        return jsonify({
            'success': True,
            'travelTips': travel_tips
        })
        
    except Exception as e:
        logger.error(f"Error generating travel tips: {str(e)}")
        return jsonify({'error': 'Failed to generate travel tips'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 