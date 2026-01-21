from app.db import init_db, street_col
from flask import Flask

app = Flask(__name__)
init_db(app)

def create_locations():
    # Clear old data
    street_col().delete_many({})

    # The data that was previously hardcoded in street.js
    locations = [
      { "id": 1, "name": "Millennium City Mall", "lat": 48.2108, "lng": 16.3725, "address": "Central Vienna", "hours": "09:00–18:00" },
      { "id": 2, "name": "Central Station",      "lat": 48.1850, "lng": 16.3747, "address": "Hbf Area",      "hours": "10:00–16:00" },
      { "id": 3, "name": "Riverside Park",       "lat": 48.2167, "lng": 16.3950, "address": "Danube Side",   "hours": "Always open" }
    ]
    
    street_col().insert_many(locations)
    print("Street locations initialized successfully!")

if __name__ == "__main__":
    create_locations()