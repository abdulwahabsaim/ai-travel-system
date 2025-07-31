from flask import Blueprint, jsonify
from datetime import datetime

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Travel Service',
        'timestamp': datetime.now().isoformat()
    })