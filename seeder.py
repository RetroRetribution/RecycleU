import uuid
import datetime
from werkzeug.security import generate_password_hash

from app.db import init_db, users_col, points_col, rewards_col, activities_col, street_col, recycle_events_col, badges_col, transactions_col
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
                {"badge_id": 1, "name": "First Recycle", "earned_on": "2024-06-02"},
                {"badge_id": 2, "name": "Collector", "earned_on": "2025-01-15"}
            ]
        })
        print("Users seeded")

    #POINTS
    if points_col().count_documents({}) == 0:
        user = users_col().find_one({})
        points_col().insert_many([
            {
                "user_id": user["id"] if user else "test_user_01",
                "points": 200,
                "timestamp": datetime.datetime(2025, 1, 14)
            },
            {
                "user_id": user["id"] if user else "test_user_01",
                "points": 150,
                "timestamp": datetime.datetime(2025, 1, 10)
            },
            {
                "user_id": user["id"] if user else "test_user_01",
                "points": 140,
                "timestamp": datetime.datetime(2024, 12, 29)
            },
            {
                "user_id": user["id"] if user else "test_user_01",
                "points": 100,
                "timestamp": datetime.datetime(2024, 12, 15)
            }
        ])
        print("Points seeded")

    #REWARDS
    if rewards_col().count_documents({}) == 0:
        rewards_col().insert_many([
            {
                "id": "spotify",
                "name": "Spotify Gift Card",
                "cost": 1000,
                "stock": 5,
                "desc": "Why not listen to music ad-free while recycling? Recycle to get one.",
                "img": "pictures/Spotify.png"
            },
            {
                "id": "google",
                "name": "Google Play Gift Card",
                "cost": 1000,
                "stock": 10,
                "desc": "As bad as Google is for the environment, money is important for our causes.",
                "img": "pictures/Google.png"
            },
            {
                "id": "apple",
                "name": "Apple Store Gift Card",
                "cost": 1000,
                "stock": 5,
                "desc": "Yes another mega tech corporation, but bide your time.",
                "img": "pictures/Apple.png"
            },
            {
                "id": "amazon",
                "name": "Amazon Gift Card",
                "cost": 1000,
                "stock": 5,
                "desc": "The worst one so far, the best to infiltrate.",
                "img": "pictures/amazon.png"
            },
            {
                "id": "cap",
                "name": "Green Cap",
                "cost": 500,
                "stock": 5,
                "desc": "Wear the logo of recycling on your head.",
                "img": "pictures/Green cap.png"
            },
            {
                "id": "bottle",
                "name": "Recycle Bottle",
                "cost": 500,
                "stock": 5,
                "desc": "Metallic and clean, hydrate the right way.",
                "img": "pictures/Blue Water Bottle.png"
            },
            {
                "id": "mug",
                "name": "Green Mug",
                "cost": 500,
                "stock": 5,
                "desc": "Metallic mug with a cute design, recycle with warmth. Have fun camping...",
                "img": "pictures/Green Mug.jpg"
            },
            {
                "id": "tshirt",
                "name": "Recycle T-Shirt",
                "cost": 500,
                "stock": 5,
                "desc": "Tshirt made from recycled materials, comfortable and eco-friendly.",
                "img": "pictures/T-shirt.png"
            },
            {
                "id": "hoodie",
                "name": "Recycle Hoodie",
                "cost": 1000,
                "stock": 5,
                "desc": "Stay warm, comfortable and eco-friendly.",
                "img": "pictures/Green hoodie.png"
            },
            {
                "id": "bag",
                "name": "Green Bag",
                "cost": 1000,
                "stock": 10,
                "desc": "Be sustainable and carry your burden with this bag.",
                "img": "pictures/Green bag.jpg"
            }
        ])
        print("Rewards seeded")

    # ACTIVITIES
    if activities_col().count_documents({}) == 0:
        activities_col().insert_many([
            {"id": "plastic", "name": "Plastic Bottle", "points": 10, "img": "pictures/plastic.png"},
            {"id": "glass", "name": "Glass Jar", "points": 15, "img": "pictures/glass.png"},
            {"id": "can", "name": "Aluminum Can", "points": 10, "img": "pictures/can.png"},
            {"id": "cardboard", "name": "Cardboard", "points": 20, "img": "pictures/cardboard.png"}
        ])
        print("Activities seeded")

    #STREET LOCATIONS
    if street_col().count_documents({}) == 0:
        street_col().insert_many([
            {"name": "City Recycle Center", "address": "Main Street 12", "hours": "09:00–18:00"},
            {"name": "Eco Drop-Off Point", "address": "Green Ave 44", "hours": "10:00–16:00"},
        ])
        print("Street locations seeded")

    # NEW: RECYCLE EVENTS
    if recycle_events_col().count_documents({}) == 0:
        user = users_col().find_one({})
        recycle_events_col().insert_many([
            {
                "user_id": user["id"] if user else "test_user_01",
                "activity": "plastic",
                "points": 100,
                "date": datetime.datetime.utcnow()
            },
            {
                "user_id": user["id"] if user else "test_user_01",
                "activity": "glass",
                "points": 150,
                "date": datetime.datetime.utcnow()
            }
        ])
        print("Recycle events seeded")

    # BADGES
    if badges_col().count_documents({}) == 0:
        badges_col().insert_many([
            {
                "badge_id": 1,
                "name": "First Recycle",
                "description": "Complete your first recycling action",
                "criteria": {"type": "earn", "count": 1}
            },
            {
                "badge_id": 2,
                "name": "Collector",
                "description": "Recycle 10 times total",
                "criteria": {"type": "earn", "count": 10}
            },
            {
                "badge_id": 3,
                "name": "Reward Seeker",
                "description": "Redeem your first reward",
                "criteria": {"type": "redeem", "count": 1}
            }
        ])
        print("Badges seeded")

    # TRANSACTIONS
    if transactions_col().count_documents({}) == 0:
        user = users_col().find_one({})
        transactions_col().insert_many([
            {
                "transaction_id": str(uuid.uuid4()),
                "user_id": user["id"] if user else "test_user_01",
                "reward_id": "1",
                "reward_name": "Recycle Hoodie",
                "used_card": False,
                "points_spent": 1000,
                "status": "completed",
                "redeemed_on": datetime.datetime.utcnow(),
                "delivery": {
                    "fullname": "Alex Green",
                    "email": "alex.green@example.com",
                    "address": "123 Green Street"
                }
            }
        ])
        print("Transactions seeded")

    print("\nDatabase seeding complete.")


if __name__ == "__main__":
    seed()
