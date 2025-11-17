from flask import Flask, render_template, jsonify
import datetime

app = Flask(__name__, template_folder='template', static_folder='static')


# ---------------------------
# FRONTEND PAGE ROUTES (ADDED)
# ---------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile_page():
    return render_template('profile.html')


@app.route('/point')
def point_page():
    return render_template('point.html')


@app.route('/reward')
def reward_page():
    return render_template('reward.html')


@app.route('/redeem')
def redeem_page():
    return render_template('redeem.html')


@app.route('/qr')
def qr_page():
    return render_template('qr.html')


@app.route('/street')
def street_page():
    return render_template('street.html')


@app.route('/about')
def about_page():
    return render_template('about.html')


# ---------------------------
# API ROUTES (UNCHANGED)
# ---------------------------

@app.route('/api/status')
def status():
    return jsonify(status='ok', time=datetime.datetime.utcnow().isoformat() + 'Z')


@app.route('/api/dummy')
def dummy():
    data = {
        "message": "Hello from dummy backend",
        "points": 123,
        "rewards": [
            {"id": 1, "name": "Reusable Bottle", "cost": 100},
            {"id": 2, "name": "Plant a Tree", "cost": 200}
        ]
    }
    return jsonify(data)


@app.route('/api/profile')
def profile():
    # Dummy user profile data
    data = {
        "id": 42,
        "name": "Alex Green",
        "email": "alex.green@example.com",
        "joined": "2024-06-01",
        "total_points": 1240,
        "badges": [
            {"id": 1, "name": "First Recycle", "earned": "2024-06-02"},
            {"id": 2, "name": "Collector", "earned": "2025-01-15"}
        ]
    }
    return jsonify(data)


@app.route('/api/points')
def points():
    # Dummy points history and summary
    data = {
        "total": 1240,
        "earned": 1400,
        "spent": 160,
        "history": [
            {"date": "2025-11-10", "change": +50, "source": "Bottle Drop"},
            {"date": "2025-11-01", "change": +200, "source": "Community Drive"},
            {"date": "2025-10-20", "change": -100, "source": "Redeemed: Reusable Bottle"}
        ]
    }
    return jsonify(data)


@app.route('/api/rewards')
def rewards():
    # Catalog of rewards the frontend can display
    data = {
        "rewards": [
            {"id": 1, "name": "Reusable Bottle", "cost": 100, "stock": 12},
            {"id": 2, "name": "Plant a Tree", "cost": 200, "stock": 5},
            {"id": 3, "name": "Discount Voucher", "cost": 300, "stock": 0}
        ]
    }
    return jsonify(data)


@app.route('/api/redeem')
def redeem():
    # Dummy redemption options and past redemptions
    data = {
        "available": [
            {"id": 1, "name": "Reusable Bottle", "cost": 100},
            {"id": 2, "name": "Plant a Tree", "cost": 200}
        ],
        "history": [
            {"id": 101, "item_id": 1, "date": "2025-10-20", "status": "completed"}
        ]
    }
    return jsonify(data)


@app.route('/api/qr')
def qr():
    # Dummy QR payload: in a real app you'd return a URL, token or base64 image
    data = {
        "code": "QR_CODE_PLACEHOLDER_ABC123",
        "value": 50,
        "expires": (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
    }
    return jsonify(data)


@app.route('/api/street')
def street():
    # Nearby drop-off locations / street collection info
    data = {
        "locations": [
            {"id": 1, "name": "Green St. Drop-Off", "address": "12 Green St", "hours": "8:00-18:00", "lat": 40.7128, "lng": -74.0060},
            {"id": 2, "name": "Westside Recycling Hub", "address": "200 West Ave", "hours": "9:00-17:00", "lat": 40.7139, "lng": -74.0100}
        ]
    }
    return jsonify(data)


@app.route('/api/about')
def about():
    data = {
        "app": "RecycleU",
        "version": "0.1.0",
        "description": "Demo backend providing sample endpoints for the RecycleU frontend.",
        "contact": "support@recycleu.example"
    }
    return jsonify(data)


# ---------------------------
# RUN SERVER
# ---------------------------

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
