from flask import request, jsonify
from points_store import get_user_points, add_points
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

@app.get("/api/points")
def api_get_points():
    # For now: single demo user (no auth yet)
    user_id = "demo"
    user = get_user_points(user_id)
    return jsonify(user)

@app.post("/api/points/add")
def api_add_points():
    user_id = "demo"
    payload = request.get_json(force=True) or {}

    location_id = int(payload.get("location_id", 0))
    delta = int(payload.get("delta", 0))
    reason = payload.get("reason", "drop_point")

    if location_id <= 0:
        return jsonify({"error": "location_id required"}), 400
    if delta == 0:
        return jsonify({"error": "delta must be non-zero"}), 400

    user = add_points(user_id=user_id, location_id=location_id, delta=delta, reason=reason)
    return jsonify(user)
