from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from app.db import users_col
from app.services.user_service import create_user

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form
    user = users_col().find_one({"email": data.get('email')})

    if not user or not check_password_hash(user['password'], data.get('password')):
        return jsonify({"error": "Invalid credentials"}), 401

    # store as string to ensure JSON-safe session
    session['user_id'] = str(user.get('id') or user.get('_id'))
    return jsonify({"id": str(user.get('id') or user.get('_id')), "email": user['email']})
