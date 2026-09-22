from difflib import SequenceMatcher
from datetime import datetime, timedelta

username_history = {}
login_history = {}


def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def track_username_change(user_id, new_username):
    if user_id not in username_history:
        username_history[user_id] = []

    username_history[user_id].append({
        "username": new_username,
        "time": datetime.now()
    })

    history = username_history[user_id]

    if len(history) < 2:
        return {
            "risk": 0,
            "status": "SAFE",
            "reasons": ["First username recorded"]
        }

    old_username = history[-2]["username"]
    score = similarity(old_username, new_username)

    risk = 0
    reasons = []

    if score < 0.35:
        risk += 25
        reasons.append("Drastic username change detected")
    elif score < 0.65:
        risk += 10
        reasons.append("Moderate username change detected")
    else:
        reasons.append("Username change is similar to previous name")

    recent_changes = [
        h for h in history
        if datetime.now() - h["time"] <= timedelta(days=14)
    ]

    if len(recent_changes) >= 3:
        risk += 15
        reasons.append("Multiple username changes within 14 days")

    status = "SUSPICIOUS" if risk >= 25 else "SAFE"

    return {
        "risk": risk,
        "status": status,
        "old_username": old_username,
        "new_username": new_username,
        "similarity": round(score * 100, 2),
        "reasons": reasons
    }


def track_login(user_id, device_id, location):
    if user_id not in login_history:
        login_history[user_id] = []

    login_history[user_id].append({
        "device_id": device_id,
        "location": location,
        "time": datetime.now()
    })

    recent_logins = [
        l for l in login_history[user_id]
        if datetime.now() - l["time"] <= timedelta(minutes=10)
    ]

    unique_devices = set(l["device_id"] for l in recent_logins)
    unique_locations = set(l["location"].lower() for l in recent_logins)

    risk = 0
    reasons = []

    if len(unique_devices) >= 2:
        risk += 20
        reasons.append("Multiple devices used in short time")

    if len(unique_locations) >= 2:
        risk += 25
        reasons.append("Multiple login locations detected in short time")

    status = "SUSPICIOUS" if risk >= 25 else "SAFE"

    return {
        "risk": risk,
        "status": status,
        "recent_login_count": len(recent_logins),
        "devices": list(unique_devices),
        "locations": list(unique_locations),
        "reasons": reasons if reasons else ["Normal login behavior"]
    }


def check_account_growth(user_id, account_age_minutes, followers_count, following_count, posts_count):
    risk = 0
    reasons = []

    account_age_minutes = int(account_age_minutes)
    followers_count = int(followers_count)
    following_count = int(following_count)
    posts_count = int(posts_count)

    if account_age_minutes <= 10 and followers_count >= 100:
        risk += 25
        reasons.append("New account gained unusually high followers within 10 minutes")

    if account_age_minutes <= 10 and following_count >= 40:
        risk += 25
        reasons.append("New account followed too many accounts in short time")

    if account_age_minutes <= 60 and followers_count >= 1000:
        risk += 35
        reasons.append("Unrealistic follower growth detected within 1 hour")

    if account_age_minutes <= 30 and posts_count >= 20:
        risk += 20
        reasons.append("Too many posts uploaded shortly after account creation")

    if risk >= 50:
        status = "HIGH RISK"
    elif risk >= 25:
        status = "SUSPICIOUS"
    else:
        status = "SAFE"

    return {
        "risk": risk,
        "status": status,
        "account_age_minutes": account_age_minutes,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count,
        "reasons": reasons if reasons else ["Normal account growth behavior"]
    }