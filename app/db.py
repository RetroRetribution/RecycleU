from pymongo import MongoClient

client = None
db = None

def init_db(app):
    global client, db
    client = MongoClient("mongodb://localhost:27017/")
    db = client["recycleU_db"]

def users_col():
    return db["users"]

def points_col():
    return db["points"]

def rewards_col():
    return db["rewards"]

def redeem_col():
    return db["redeem"]

def street_col():
    return db["street"]

def recycle_events_col():
    """Return the recycle_events collection."""
    return db["recycle_events"]


def badges_col():
    """Return the badges collection."""
    return db["badges"]


def transactions_col():
    """Return the transactions collection."""
    return db["transactions"]
