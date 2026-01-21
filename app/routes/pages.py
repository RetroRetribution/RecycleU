from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import datetime

from app.db import rewards_col, users_col, activities_col, points_col
from app.services.user_service import process_redemption, process_earning


pages_bp = Blueprint('pages', __name__)


# ----------------------------
# Helpers
# ----------------------------
def _get_current_user_id():
    """
    Prefer session user; otherwise fall back to the first seeded user.
    This keeps everything working even without auth/login.
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
    # legacy/static points page (your real drop-point view is /drop-point/<id>)
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


@pages_bp.route("/drop-point/<int:location_id>")
def drop_point_page(location_id):
    names = {1: "Millennium City Mall", 2: "Central Station", 3: "Riverside Park"}
    return render_template(
        "points.html",
        location_id=location_id,
        location_name=names.get(location_id, "Drop Point")
    )


# ----------------------------
# Redemption
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

        # Keep your teammate's service logic untouched
        process_redemption(user_id, item, delivery_data, payment_method)

        return redirect(url_for('pages.redemption_success', name=delivery_data['fullname']))

    return render_template('redemption.html', item=item)


@pages_bp.route('/redemption-success')
def redemption_success():
    name = request.args.get('name', 'User')
    return render_template('redemption_success.html', name=name)


# ----------------------------
# Recycling
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

        # Keep service logic untouched
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
# Donations (community pool)
# ----------------------------
@pages_bp.route('/donate', methods=['POST'])
def donate_points():
    data = request.get_json(force=True) or {}
    points_to_donate = int(data.get('points', 0))

    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"success": False, "error": "No user found"}), 500

    donation = {
        "user_id": user_id,
        "points": points_to_donate,
        "reason": "donation",
        "timestamp": datetime.datetime.utcnow()
    }
    points_col().insert_one(donation)

    total_donated = points_col().aggregate([
        {"$match": {"reason": "donation"}},
        {"$group": {"_id": None, "total": {"$sum": "$points"}}}
    ])
    total_list = list(total_donated)
    total = total_list[0]["total"] if total_list else 0

    return jsonify({
        "success": True,
        "message": f"Donated {points_to_donate} points!",
        "community_total": total
    })


# ----------------------------
# Unified Points API (Mongo-backed)
# This replaces points_store completely.
# Drop points + profile + redemption all read the same wallet: users.total_points
# ----------------------------
@pages_bp.route("/api/points", methods=["GET"])
def api_get_points():
    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"error": "No user found. Run seeder.py"}), 500

    user = users_col().find_one({"id": user_id}, {"_id": 0, "id": 1, "total_points": 1})
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "user_id": user["id"],
        "total": int(user.get("total_points", 0))
    })


@pages_bp.route("/api/points/add", methods=["POST"])
def api_add_points():
    payload = request.get_json(force=True) or {}

    location_id = int(payload.get("location_id", 0))
    delta = int(payload.get("delta", 0))
    reason = payload.get("reason", "drop_point")

    if location_id <= 0:
        return jsonify({"error": "location_id required"}), 400
    if delta == 0:
        return jsonify({"error": "delta must be non-zero"}), 400

    user_id = _get_current_user_id()
    if not user_id:
        return jsonify({"error": "No user found. Run seeder.py"}), 500

    user = users_col().find_one({"id": user_id}, {"_id": 0, "total_points": 1})
    if not user:
        return jsonify({"error": "User not found"}), 404

    current_total = int(user.get("total_points", 0))
    if delta < 0 and current_total + delta < 0:
        return jsonify({"error": "Insufficient points", "total": current_total}), 409

    # Update wallet
    users_col().update_one({"id": user_id}, {"$inc": {"total_points": delta}})

    # Optional log (useful for history later)
    points_col().insert_one({
        "user_id": user_id,
        "points": delta,
        "reason": reason,
        "location_id": location_id,
        "timestamp": datetime.datetime.utcnow()
    })

    updated = users_col().find_one({"id": user_id}, {"_id": 0, "total_points": 1})
    return jsonify({
        "user_id": user_id,
        "total": int(updated.get("total_points", 0))
    })
