from flask import Blueprint, render_template, request, redirect, url_for
from app.db import rewards_col

pages_bp = Blueprint('pages', __name__)

@pages_bp.route('/')
def index():
    return render_template('index.html')

@pages_bp.route('/points')
def points_page():
    return render_template('points.html')

@pages_bp.route('/profile')
def profile_page():
    return render_template('profile.html')

@pages_bp.route('/rewardss')
def rewards_page():
    return render_template('rewardss.html')

@pages_bp.route('/rewards')
def redeem_page():
    rewards_list = list(rewards_col().find({}, {"_id": 0}))
    # pass the list to the template as `items` so the Jinja template can iterate over it
    return render_template('rewards.html', items=rewards_list)

@pages_bp.route('/qr')
def qr_page():
    return render_template('qr.html')

@pages_bp.route('/street')
def street_page():
    return render_template('street.html')

@pages_bp.route('/about')
def about_page():
    return render_template('about.html')

@pages_bp.route('/redemption/<reward_id>', methods=['GET', 'POST'])
def redemption(reward_id):
    item = rewards_col().find_one({"id": reward_id}, {"_id": 0})
    
    if not item:
        return "Reward not found", 404

    if request.method == 'POST':
        fullname = request.form.get('fullname')
        return redirect(url_for('pages.redemption_success', name=fullname))
        
    return render_template('redemption.html', item=item)

@pages_bp.route('/redemption-success')
def redemption_success():
    name = request.args.get('name', 'User')
    return render_template('redemption_success.html', name=name)