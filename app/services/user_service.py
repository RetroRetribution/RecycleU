import uuid, datetime
from werkzeug.security import generate_password_hash
from app.db import users_col

def create_user(name, email, password):
    if users_col().find_one({"email": email}):
        return None

    user = {
        "id": uuid.uuid4().hex,
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "joined": datetime.datetime.utcnow().date().isoformat(),
        "total_points": 0,
        "badges": []
    }

    users_col().insert_one(user)
    return user
