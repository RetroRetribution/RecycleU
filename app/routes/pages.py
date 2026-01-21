from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import datetime

from app.db import rewards_col, users_col, activities_col, points_col, street_col
from app.services.user_service import process_redemption, process_earning


pages_bp = Blueprint('pages', __name__)


# ----------------------------
# Helpers
# ----------------------------
def _get_current_user_id():
    """
    Prefer session user; otherwise fall back to the first seeded user.
    """
    user_id = session.get("user_id")
    if user_id:
        return user_id

    seeded = users_col().find_one({})
    if seeded and "id" in seeded:
        return seeded["id"]

    return None


# ----------------------------
# Page routes
# ----------------------------
@pages_bp.route('/')
def index():
    return render_template('index.html')


@pages_bp.route('/points')
def points_page():
    # Pass location_id=1 so the page knows where to assign points
    return render_template('points.html', location_id=1, location_name="Millennium City Mall")


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


@pages_bp.route("/drop-point/<int:location_id>")
def drop_point_page(location_id):
    names = {1: "Millennium City Mall", 2: "Central Station", 3: "Riverside Park"}
    return render_template(
        "points.html",
        location_id=location_id,
        location_name=names.get(location_id, "Drop Point")
    )


# ----------------------------
# Redemption (Spends Points)
# ----------------------------
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

        user_id = _get_current_user_id()
        if not user_id:
            return jsonify({"error": "No user found. Run seeder.py"}), 500

        user = users_col().find_one({"id": user_id})
        if not user:
            return jsonify({"error": "User not found"}), 404

        if payment_method == 'points':
            user_points = int(user.get('total_points', 0))
            item_cost = int(item.get('cost', 0))

            if user_points < item_cost:
                return jsonify({
                    "error": f"Insufficient points. You have {user_points}, need {item_cost}."
                }), 400

        # process_redemption logic handles the deduction
        process_redemption(user_id, item, delivery_data, payment_method)

        return redirect(url_for('pages.redemption_success', name=delivery_data['fullname']))

    return render_template('redemption.html', item=item)


@pages_bp.route('/redemption-success')
def redemption_success():
    name = request.args.get('name', 'User')
    return render_template('redemption_success.html', name=name)


# ----------------------------
# Recycling (EARNS Points)
# ----------------------------
@pages_bp.route('/recycle', methods=['GET', 'POST'])
def recycle_page():
    activities = list(activities_col().find({}, {"_id": 0}))

    if request.method == 'POST':
        activity_id = request.form.get('activity_id')
        points_to_add = request.form.get('points_value')
        user_id = _get_current_user_id()

        if not user_id:
            return "No user found. Run seeder.py", 500

        # process_earning logic handles ADDING points to the user
        process_earning(user_id, activity_id, points_to_add)

        print(f"Added {points_to_add} points to {user_id} for {activity_id}")
        return redirect(url_for('pages.recycle_page'))

    user_id = _get_current_user_id()
    user_points = 0

    if user_id:
        user = users_col().find_one({"id": user_id}, {"_id": 0})
        if user:
            user_points = int(user.get('total_points', 0))

    return render_template('recycle.html', activities=activities, user_points=user_points)


# ----------------------------
# Drop Points (Community Donation)
# ----------------------------
@pages_bp.route('/donate', methods=['POST'])
def donate_points():
    """Simple donation route (optional)"""
    data = request.get_json(force=True) or {}
    points_to_donate = int(data.get('points', 0))

    user_id = _get_current_user_id()
    
    # Just add to community pool
    donation = {
        "user_id": user_id if user_id else "anonymous",
        "points": points_to_donate,
        "reason": "donation",
        "timestamp": datetime.datetime.utcnow()
    }
    points_col().insert_one(donation)

    return jsonify({
        "success": True,
        "message": f"Donated {points_to_donate} points!"
    })


@pages_bp.route("/api/points/add", methods=["POST"])
def api_add_points():
   # Handle adding points via API (either QR scan or Drop Point)
   #If the reason is "qr_upload", points go to user's personal wallet.
   #If the reason is "drop_point", points go to community bank for that location and for now, do not affect user's personal wallet.
    payload = request.get_json(force=True) or {}

    location_id = int(payload.get("location_id", 0))
    points = int(payload.get("points", 0))
    reason = payload.get("reason", "drop_point")

    if points <= 0:
        return jsonify({"error": "points must be greater than 0"}), 400

    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"error": "No user found"}), 404

    if reason == "qr_upload":
        process_earning(user_id, "qr_scan", points)
        
        user = users_col().find_one({"id": user_id})
        new_total = user.get("total_points", 0)

        return jsonify({
            "success": True, 
            "message": f"Earned {points} points!",
            "total": new_total
        })

    else:
        if location_id <= 0:
            return jsonify({"error": "location_id required for drop points"}), 400

        # Insert DIRECTLY into Community Points Collection (User wallet unchanged)
        points_col().insert_one({
            "user_id": user_id,
            "points": points,
            "reason": reason,
            "location_id": location_id,
            "timestamp": datetime.datetime.utcnow()
        })

        return jsonify({
            "success": True, 
            "message": "Added to community bank",
            "location_id": location_id
        })

@pages_bp.route("/api/points/location/<int:location_id>", methods=["GET"])
def api_get_location_total(location_id):
    """
    Returns the total community points accumulated at this specific location.
    """
    pipeline = [
        {"$match": {"location_id": location_id}},
        {"$group": {"_id": None, "total": {"$sum": "$points"}}}
    ]
    
    result = list(points_col().aggregate(pipeline))
    total_points = result[0]["total"] if result else 0
    
    return jsonify({
        "location_id": location_id, 
        "total": total_points
    })


@pages_bp.route("/api/street", methods=["GET"])
def api_get_street():
    locations = list(street_col().find({}, {"_id": 0}))
    return jsonify(locations)