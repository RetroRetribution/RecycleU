import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash
from app.db import users_col, transactions_col, badges_col, recycle_events_col

def check_and_award_badges(user_id):
    user = users_col().find_one({"id": user_id})
    if not user:
        return

    current_badge_ids = [b['badge_id'] for b in user.get('badges', [])]
    

    recycle_count = recycle_events_col().count_documents({"user_id": user_id})
    

    redeem_count = transactions_col().count_documents({"user_id": user_id, "reward_id": {"$exists": True}})

    all_badges = badges_col().find({})

    for badge in all_badges:
        b_id = badge['badge_id']
        criteria = badge.get('criteria', {})
        
        if b_id in current_badge_ids:
            continue


        if criteria.get('type') == 'earn' and recycle_count >= criteria.get('count', 0):
            award_badge(user_id, badge)


        elif criteria.get('type') == 'redeem' and redeem_count >= criteria.get('count', 0):
            award_badge(user_id, badge)

def award_badge(user_id, badge):
    new_badge_entry = {
        "badge_id": badge['badge_id'],
        "name": badge['name'],
        "earned_on": datetime.now().strftime("%Y-%m-%d")
    }
    
    users_col().update_one(
        {"id": user_id},
        {"$push": {"badges": new_badge_entry}}
    )
    print(f"User {user_id} earned badge: {badge['name']}")




def create_user(name, email, password):
    if users_col().find_one({"email": email}):
        return None

    user = {
        "id": uuid.uuid4().hex,
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "joined": datetime.utcnow().date().isoformat(),
        "total_points": 0,
        "badges": []
    }
    users_col().insert_one(user)
    return user

def process_redemption(user_id, item, delivery_data, payment_method):
    points_cost = int(item.get('cost', 0))
    points_spent = points_cost if payment_method == 'points' else 0
    is_card_payment = (payment_method == 'card')

    transaction_data = {
        "transaction_id": str(uuid.uuid4()),
        "user_id": user_id,
        "reward_id": item['id'],
        "reward_name": item['name'],
        "used_card": is_card_payment,
        "points_spent": points_spent,
        "status": "completed",
        "redeemed_on": datetime.now(),
        "delivery": delivery_data
    }

    transactions_col().insert_one(transaction_data)

    if payment_method == 'points':
        users_col().update_one(
            {"id": user_id},
            {"$inc": {"total_points": -points_spent}}
        )

    check_and_award_badges(user_id)
    return transaction_data['transaction_id']

def process_earning(user_id, activity_id, points_earned):

    event_data = {
        "user_id": user_id,
        "activity": activity_id,
        "points": int(points_earned),
        "date": datetime.now()

    }

    recycle_events_col().insert_one(event_data)

    users_col().update_one(
        {"id": user_id}, 
        {"$inc": {"total_points": int(points_earned)}}
    )
    
    check_and_award_badges(user_id)
    
    return True