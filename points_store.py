import json
import os
from threading import Lock
from datetime import datetime

_LOCK = Lock()

def _store_path():
    # points_data.json lives next to run.py (safe and simple)
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "points_data.json")

def _load():
    path = _store_path()
    if not os.path.exists(path):
        return {"users": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data):
    path = _store_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_user_points(user_id: str):
    with _LOCK:
        data = _load()
        user = data["users"].get(user_id)
        if not user:
            user = {
                "total": 0,
                "by_location": {},   # location_id -> points
                "history": []        # list of events
            }
            data["users"][user_id] = user
            _save(data)
        return user

def add_points(user_id: str, location_id: int, delta: int, reason: str = "drop_point"):
    if not isinstance(delta, int):
        raise ValueError("delta must be int")

    with _LOCK:
        data = _load()
        user = data["users"].get(user_id)
        if not user:
            user = {"total": 0, "by_location": {}, "history": []}
            data["users"][user_id] = user

        user["total"] = int(user.get("total", 0)) + delta

        loc_key = str(location_id)
        by_loc = user.get("by_location", {})
        by_loc[loc_key] = int(by_loc.get(loc_key, 0)) + delta
        user["by_location"] = by_loc

        user["history"].insert(0, {
            "ts": datetime.utcnow().isoformat() + "Z",
            "location_id": location_id,
            "delta": delta,
            "reason": reason
        })

        # keep history small
        user["history"] = user["history"][:50]

        _save(data)
        return user
