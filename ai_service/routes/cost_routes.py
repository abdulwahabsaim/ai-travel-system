from flask import Blueprint, request, jsonify
import logging
from ai_modules.cost_predictor import CostPredictor

cost_bp = Blueprint('cost_bp', __name__)
logger = logging.getLogger(__name__)
cost_predictor = CostPredictor()

@cost_bp.route('/predict-costs', methods=['POST'])
def predict_costs():
    try:
        data = request.get_json()
        cost_prediction = cost_predictor.predict(
            destination=data.get('destination'),
            duration=data.get('duration'),
            travel_style=data.get('travelStyle', 'balanced'),
            group_size=data.get('groupSize', 1),
            season=data.get('season')
        )
        return jsonify({'success': True, 'costPrediction': cost_prediction})
    except Exception as e:
        logger.error(f"Error predicting costs: {str(e)}")
        return jsonify({'error': 'Failed to predict costs'}), 500

@cost_bp.route('/optimize-budget', methods=['POST'])
def optimize_budget():
    try:
        data = request.get_json()
        budget_optimization = cost_predictor.optimize_budget(
            total_budget=data.get('totalBudget'),
            destination=data.get('destination'),
            duration=data.get('duration'),
            preferences=data.get('preferences', {})
        )
        return jsonify({'success': True, 'budgetOptimization': budget_optimization})
    except Exception as e:
        logger.error(f"Error optimizing budget: {str(e)}")
        return jsonify({'error': 'Failed to optimize budget'}), 500