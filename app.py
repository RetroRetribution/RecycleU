from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import datetime

# After taking time to figure MongoDB out, the follwing is the MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["recycleU_db"]

users_col = db["users"]
points_col = db["points"]
rewards_col = db["rewards"]
redeem_col = db["redeem"]
street_col = db["street"]

app = Flask(__name__, template_folder='template', static_folder='static')

# The template routes display the HTML pages
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

# The API routes provide JSON data to the fronted-end of website

@app.route('/api/status')
def api_status():
    return jsonify({"status": "running", "message": "API is operational"})

@app.route('/api/dummy')
def api_dummy():
    return jsonify({"message": "Hello from the backend!"})

@app.route('/api/profile')
def api_profile():
    user = users_col.find_one({}, {"_id": 0})

    if not user:
        return jsonify({"error": "No profile found"}), 404

    return jsonify(user)



@app.route('/api/points')
def points():
    # Fetch points data from MongoDB itself
    data = points_col.find_one({}, {"_id": 0})
    
    if not data:
        # Dummy data as fallback if MongoDB is empty
        data = {
            "total": 1240,
            "earned": 1500,
            "spent": 260,
            "history": [
                {"date": "2025-01-14", "change": "+200", "source": "Bottle Return"},
                {"date": "2025-01-10", "change": "+150", "source": "Paper Recycling"},
                {"date": "2025-01-08", "change": "-100", "source": "Reward Purchase"},
                {"date": "2024-12-29", "change": "+140", "source": "Glass Recycling"},
            ]
        }
    
    return jsonify(data)

@app.route('/api/rewards')
def api_rewards():
    rewards = list(rewards_col.find({}, {"_id": 0}))
    return jsonify({"rewards": rewards})


@app.route('/api/redeem')
def api_redeem():
    data = redeem_col.find_one({}, {"_id": 0})

    if not data:
        return jsonify({"error": "No redeem data found"}), 404

    return jsonify(data)


@app.route('/api/qr')
def qr():
    # Dummy QR payload: in a real app you'd return a URL, this is for the sake of simplicity
    data = {
        "code": "QR_CODE_PLACEHOLDER_ABC123",
        "value": 50,
        "expires": (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
    }
    return jsonify(data)


@app.route('/api/street')
def api_street():
    locations = list(street_col.find({}, {"_id": 0}))
    return jsonify({"locations": locations})


@app.route('/api/about')
def api_about():
    return jsonify({
        "app": "RecycleU",
        "version": "1.0.0",
        "description": "A simple recycling gamification app.",
        "contact": "support@recycleu.app"
    })

from flask import Flask, render_template, request, redirect, url_for

@app.route('/redemption/<int:reward_id>', methods=['GET', 'POST'])
def redemption(reward_id):
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        address = request.form.get('address')
        payment_method = request.form.get('payment_method')
        card_number = request.form.get('card_number')
        cvv = request.form.get('cvv')

        # TODO: Insert into database when ready
        print("Redemption submitted:")
        print("Name:", fullname)
        print("Email:", email)
        print("Address:", address)
        print("Payment method:", payment_method)

        return redirect(url_for('redemption_success', name=fullname))

    return render_template('redemption.html', reward_id=reward_id)


@app.route('/redemption-success')
def redemption_success():
    name = request.args.get('name', 'User')
    return render_template('redemption_success.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)