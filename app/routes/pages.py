from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.db import rewards_col, users_col, activities_col
from app.services.user_service import process_redemption, process_earning
import datetime

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/points')
def points_page():
    return render_template('points.html')

@pages_bp.route('/profile')
def profile_page():
    return render_template('profile.html')

@pages_bp.route('/rewardss')
def rewardss_page():
    return render_template('rewardss.html')

@pages_bp.route('/rewards')
def rewards_page():
    rewards_list = list(rewards_col().find({}, {"_id": 0}))
    return render_template('rewards.html', items=rewards_list)

@pages_bp.route('/qr')
def qr_page():
    return render_template('qr.html')

@pages_bp.route('/street')
def street_page():
    return render_template('street.html')

@pages_bp.route('/about')
def about_page():
    return render_template('about.html')

@pages_bp.route('/redemption/<reward_id>', methods=['GET', 'POST'])
def redemption(reward_id):
    item = rewards_col().find_one({"id": reward_id}, {"_id": 0})
    
    if not item:
        return "Reward not found", 404

    if request.method == 'POST':
    
        delivery_data = {
            "fullname": request.form.get('fullname'),
            "email": request.form.get('email'),
            "address": request.form.get('address')
        }
        payment_method = request.form.get('payment_method')
        
        user_id = session.get('user_id', 'test_user_01')
        user = users_col().find_one({"id": user_id})

        if payment_method == 'points':
            user_points = user.get('total_points', 0) if user else 0
            item_cost = int(item.get('cost', 0))
            
            if user_points < item_cost:
                return jsonify({"error": f"Insufficient points. You have {user_points}, need {item_cost}."}), 400

        process_redemption(user_id, item, delivery_data, payment_method)

        return redirect(url_for('pages.redemption_success', name=delivery_data['fullname']))
        
    return render_template('redemption.html', item=item)

@pages_bp.route('/recycle', methods=['GET', 'POST'])
def recycle_page():
    activities = list(activities_col().find({}, {"_id": 0}))

    if request.method == 'POST':
        activity_id = request.form.get('activity_id')
        points_to_add = request.form.get('points_value')
        user_id = session.get('user_id', 'test_user_01') 

        process_earning(user_id, activity_id, points_to_add)
        
        print(f"Added {points_to_add} points to {user_id} for {activity_id}")
        
        return redirect(url_for('pages.recycle_page'))

    user_id = session.get('user_id', 'test_user_01')
    user_points = 0
    if user_id:
        user = users_col().find_one({"id": user_id}, {"_id": 0})
        if user:
            user_points = user.get('total_points', 0)

    return render_template('recycle.html', activities=activities, user_points=user_points)

@pages_bp.route('/redemption-success')
def redemption_success():
    name = request.args.get('name', 'User')
    return render_template('redemption_success.html', name=name)

@pages_bp.route('/donate', methods=['POST'])
def donate_points():
    data = request.get_json()
    points_to_donate = int(data.get('points', 0))
    
    user_id = session.get('user_id', 'test_user_01')

    from app.db import points_col
    donation = {
        "user_id": user_id,
        "points": points_to_donate,
        "timestamp": datetime.datetime.utcnow()
    }
    points_col().insert_one(donation)

    total_donated = points_col().aggregate([
        {"$group": {"_id": None, "total": {"$sum": "$points"}}}
    ])
    total = list(total_donated)[0]["total"] if total_donated else 0

    return jsonify({"success": True, "message": f"Donated {points_to_donate} points!", "community_total": total})