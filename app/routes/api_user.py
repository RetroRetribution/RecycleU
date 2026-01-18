from flask import Blueprint, request, jsonify, session
from app.services.user_service import create_user
from app.db import users_col

user_api_bp = Blueprint('user_api', __name__, url_prefix='/api')

@user_api_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

   
    user = users_col().find_one(
        {"id": session['user_id']},
        {"_id": 0, "password": 0}
    )

    if not user:
        session.clear()
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)

@user_api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400

    try:
        user = create_user(name, email, password)
        if not user:
            return jsonify({"error": "Email already registered"}), 409


        user_id = user.get('id') or user.get('_id')
        session['user_id'] = str(user_id)


        response = {
            "id": str(user_id),
            "email": user.get('email'),
            "name": user.get('name')
        }
        return jsonify(response), 201

    except Exception as exc:

        return jsonify({"error": "Internal server error"}), 500

@user_api_bp.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

@user_api_bp.route('/debug/clear_users')
def debug_clear_users():
    result = users_col().delete_many({})
    return jsonify({"message": f"Deleted {result.deleted_count} user(s)."}), 200