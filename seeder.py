import uuid
import datetime
from werkzeug.security import generate_password_hash

from app.db import init_db, users_col, points_col, rewards_col, redeem_col, street_col, recycle_events_col, badges_col, transactions_col
from flask import Flask


def seed():
    app = Flask(__name__)
    init_db(app)

    #USERS
    if users_col().count_documents({}) == 0:
        users_col().insert_one({
            "id": uuid.uuid4().hex,
            "name": "Alex Green",
            "email": "alex.green@example.com",
            "password": generate_password_hash("password123"),
            "joined": "2024-06-01",
            "total_points": 1240,
            "badges": [
                {"name": "First Recycle", "earned": "2024-06-02"},
                {"name": "Collector", "earned": "2025-01-15"}
            ]
        })
        print("Users seeded")

    #POINTS
    if points_col().count_documents({}) == 0:
        points_col().insert_one({
            "total": 1240,
            "earned": 1500,
            "spent": 260,
            "history": [
                {"date": "2025-01-14", "change": "+200", "source": "Bottle Return"},
                {"date": "2025-01-10", "change": "+150", "source": "Paper Recycling"},
                {"date": "2025-01-08", "change": "-100", "source": "Reward Purchase"},
                {"date": "2024-12-29", "change": "+140", "source": "Glass Recycling"},
            ]
        })
        print("Points seeded")

    #REWARDS
    if rewards_col().count_documents({}) == 0:
        rewards_col().insert_many([
            {"id": 1, "name": "Recycle Hoodie", "cost": 1000, "stock": 5},
            {"id": 2, "name": "Eco Tote Bag", "cost": 700, "stock": 10},
            {"id": 3, "name": "Metal Bottle", "cost": 500, "stock": 0}
        ])
        print("Rewards seeded")

    #REDEEM
    if redeem_col().count_documents({}) == 0:
        redeem_col().insert_one({
            "available": [
                {"id": 1, "name": "Reusable Bottle", "cost": 100},
                {"id": 2, "name": "Plant a Tree", "cost": 200}
            ],
            "history": [
                {"id": 1, "name": "Park Cleanup Pass", "redeemed_on": "2024-12-20"}
            ]
        })
        print("Redeem data seeded")

    #STREET LOCATIONS
    if street_col().count_documents({}) == 0:
        street_col().insert_many([
            {"name": "City Recycle Center", "address": "Main Street 12", "hours": "09:00–18:00"},
            {"name": "Eco Drop-Off Point", "address": "Green Ave 44", "hours": "10:00–16:00"},
        ])
        print("Street locations seeded")

    # NEW: RECYCLE EVENTS
    if recycle_events_col().count_documents({}) == 0:
        user = users_col().find_one({})  # use any existing user if present
        recycle_events_col().insert_one({
            "event_id": uuid.uuid4().hex,
            "user_id": user["id"] if user else None,
            "type": "Bottle Recycling",
            "material": "Plastic",
            "quantity": 20,
            "points_awarded": 200,
            "location": "City Recycle Center",
            "method": "QR Scan",
            "timestamp": datetime.datetime.utcnow()
        })
        print("Recycle events seeded")

    # NEW: BADGES
    if badges_col().count_documents({}) == 0:
        badges_col().insert_many([
            {
                "badge_id": 1,
                "name": "First Recycle",
                "description": "Complete your first recycling action",
                "criteria": {"min_events": 1}
            },
            {
                "badge_id": 2,
                "name": "Collector",
                "description": "Recycle 100 items total",
                "criteria": {"min_items": 100}
            }
        ])
        print("Badges seeded")

    # NEW: TRANSACTIONS
    if transactions_col().count_documents({}) == 0:
        user = users_col().find_one({})
        transactions_col().insert_one({
            "transaction_id": uuid.uuid4().hex,
            "user_id": user["id"] if user else None,
            "reward_id": 1,
            "reward_name": "Recycle Hoodie",
            "points_spent": 1000,
            "status": "completed",
            "redeemed_on": datetime.datetime.utcnow(),
            "delivery": {
                "method": "shipping",
                "address": "123 Green Street"
            }
        })
        print("Transactions seeded")

    print("\nDatabase seeding complete.")


if __name__ == "__main__":
    seed()
