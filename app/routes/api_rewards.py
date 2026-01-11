from flask import Blueprint, jsonify
from app.db import rewards_col, redeem_col, points_col, street_col

rewards_api_bp = Blueprint('rewards_api', __name__, url_prefix='/api')

@rewards_api_bp.route('/rewards')
def get_rewards():
    rewards = list(rewards_col().find({}, {"_id": 0}))
    return jsonify({"rewards": rewards})

@rewards_api_bp.route('/redeem')
def get_redeem():
    data = redeem_col().find_one({}, {"_id": 0})
    if not data:
        return jsonify({"error": "No redeem data found"}), 404
    return jsonify(data)

@rewards_api_bp.route('/points')
def get_points():
    data = points_col().find_one({}, {"_id": 0})
    if not data:
        data = {
            "total": 1240,
            "earned": 1500,
            "spent": 260,
            "history": [
                {"date": "2025-01-14", "change": "+200", "source": "Bottle Return"},
                {"date": "2025-01-10", "change": "+150", "source": "Paper Recycling"},
                {"date": "2025-01-08", "change": "-100", "source": "Reward Purchase"},
                {"date": "2024-12-29", "change": "+140", "source": "Glass Recycling"},
            ]
        }
    return jsonify(data)

@rewards_api_bp.route('/qr')
def get_qr():
    data = {
        "code": "QR_CODE_PLACEHOLDER_ABC123",
        "value": 50,
        "expires": "2099-12-31T00:00:00Z"
    }
    return jsonify(data)

@rewards_api_bp.route('/street')
def get_street():
    locations = list(street_col().find({}, {"_id": 0}))
    return jsonify({"locations": locations})

@rewards_api_bp.route('/about')
def about():
    return jsonify({
        "app": "RecycleU",
        "version": "1.0.0",
        "description": "A simple recycling gamification app.",
        "contact": "support@recycleu.app"
    })