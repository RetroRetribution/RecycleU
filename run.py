from flask import request, jsonify
from datetime import datetime
from app import create_app
from app.db import init_db, users_col, points_col

app = create_app()
init_db(app)

def _get_demo_user():
    # For now we use the first seeded user (Alex Green)
    user = users_col().find_one({})
    return user

@app.route("/api/points", methods=["GET"])
def api_get_points():
    user = _get_demo_user()
    if not user:
        return jsonify({"error": "No user found. Run seeder.py"}), 500

    return jsonify({
        "user_id": user["id"],
        "total": int(user.get("total_points", 0))
    })

@app.route("/api/points/add", methods=["POST"])
def api_add_points():
    user = _get_demo_user()
    if not user:
        return jsonify({"error": "No user found. Run seeder.py"}), 500

    payload = request.get_json(force=True) or {}
    location_id = payload.get("location_id", None)
    delta = int(payload.get("delta", 0))
    reason = payload.get("reason", "drop_point")

    if delta == 0:
        return jsonify({"error": "delta must be non-zero"}), 400

    # Deduct protection (so redemption can't go negative)
    current_total = int(user.get("total_points", 0))
    if delta < 0 and current_total + delta < 0:
        return jsonify({"error": "Insufficient points", "total": current_total}), 409

    # Update user's total points
    users_col().update_one(
        {"id": user["id"]},
        {"$inc": {"total_points": delta}}
    )

    # Log in points collection for history/audit
    points_col().insert_one({
        "user_id": user["id"],
        "points": delta,
        "reason": reason,
        "location_id": location_id,
        "timestamp": datetime.utcnow()
    })

    # Return updated total
    updated = users_col().find_one({"id": user["id"]})
    return jsonify({
        "user_id": user["id"],
        "total": int(updated.get("total_points", 0))
    })

if __name__ == "__main__":
    app.run(debug=True)
