from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

# ---------------------------------------
#   TEMPLATE ROUTES (FINAL — CORRECT)
# ---------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/points')
def points_page():
    return render_template('points.html')

@app.route('/rewards')
def rewards_page():
    return render_template('rewards.html')

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

# ---------------------------------------
#              API ROUTES
#   (Your teammate's work — UNTOUCHED)
# ---------------------------------------

@app.route('/api/status')
def api_status():
    return jsonify({"status": "running", "message": "API is operational"})

@app.route('/api/dummy')
def api_dummy():
    return jsonify({"message": "Hello from the backend!"})

@app.route('/api/profile')
def api_profile():
    return jsonify({
        "name": "Alex Green",
        "email": "alex.green@example.com",
        "joined": "2024-06-01",
        "total_points": 1240,
        "badges": [
            {"name": "First Recycle", "earned": "2024-06-02"},
            {"name": "Collector", "earned": "2025-01-15"}
        ]
    })

@app.route('/api/points')
def api_points():
    return jsonify({
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

@app.route('/api/rewards')
def api_rewards():
    return jsonify({
        "rewards": [
            {"id": 1, "name": "Recycle Hoodie", "cost": 1000, "stock": 5},
            {"id": 2, "name": "Eco Tote Bag", "cost": 700, "stock": 10},
            {"id": 3, "name": "Metal Bottle", "cost": 500, "stock": 0}
        ]
    })

@app.route('/api/redeem')
def api_redeem():
    return jsonify({
        "options": [
            {"id": 1, "name": "Plant-a-Tree", "cost": 300},
            {"id": 2, "name": "Park Cleanup Pass", "cost": 150},
        ],
        "history": [
            {"id": 1, "name": "Park Cleanup Pass", "redeemed_on": "2024-12-20"},
        ]
    })

@app.route('/api/qr')
def api_qr():
    return jsonify({
        "token": "QR-9832-ABCD-2025",
        "expires_at": "2025-01-22T18:30:00"
    })

@app.route('/api/street')
def api_street():
    return jsonify({
        "locations": [
            {"name": "City Recycle Center", "address": "Main Street 12", "hours": "09:00–18:00"},
            {"name": "Eco Drop-Off Point", "address": "Green Ave 44", "hours": "10:00–16:00"},
        ]
    })

@app.route('/api/about')
def api_about():
    return jsonify({
        "app": "RecycleU",
        "version": "1.0.0",
        "description": "A simple recycling gamification app.",
        "contact": "support@recycleu.app"
    })


# ---------------------------------------
#          RUN FLASK SERVER
# ---------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
