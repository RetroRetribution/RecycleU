from pymongo import MongoClient
from werkzeug.security import generate_password_hash
import datetime
import uuid

client = MongoClient("mongodb://localhost:27017/")
db = client["recycleU_db"]

# Seed an initial user with randomized id and hashed password
db.users.insert_one({
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

db.points.insert_one({
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

db.rewards.insert_many([
    {"id": 1, "name": "Recycle Hoodie", "cost": 1000, "stock": 5},
    {"id": 2, "name": "Eco Tote Bag", "cost": 700, "stock": 10},
    {"id": 3, "name": "Metal Bottle", "cost": 500, "stock": 0}
])

db.redeem.insert_one({
    "available": [
        {"id": 1, "name": "Reusable Bottle", "cost": 100},
        {"id": 2, "name": "Plant a Tree", "cost": 200}
    ],
    "history": [
        {"id": 1, "name": "Park Cleanup Pass", "redeemed_on": "2024-12-20"}
    ]
})

db.street.insert_many([
    {"name": "City Recycle Center", "address": "Main Street 12", "hours": "09:00–18:00"},
    {"name": "Eco Drop-Off Point", "address": "Green Ave 44", "hours": "10:00–16:00"},
])
