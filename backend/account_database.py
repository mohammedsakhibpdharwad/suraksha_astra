import json
import random
from pathlib import Path

DB_PATH = Path("backend/accounts_db.json")


sample_users = [
    "tharun_gk", "saqib_07", "suchitra_ai", "chetana_tech", "priyanka_22",
    "rahul_dev", "kiran_photos", "presidency_updates", "cid_karnataka",
    "insta_support_fake", "m_sakhib", "user123", "dark_user99"
]


def create_random_database():
    data = {}

    for username in sample_users:
        account_age = random.choice([5, 8, 12, 30, 60, 1440, 5000])
        followers = random.choice([10, 25, 80, 150, 500, 1200, 5000])
        following = random.choice([5, 12, 30, 45, 80, 150])
        posts = random.choice([0, 2, 5, 12, 25, 40])

        devices = random.sample(
            ["phone_1", "phone_2", "laptop_1", "tablet_1", "unknown_device"],
            random.randint(1, 3)
        )

        locations = random.sample(
            ["Bengaluru", "Delhi", "Mumbai", "Belagavi", "Hyderabad"],
            random.randint(1, 3)
        )

        username_history = random.sample(
            [username, username + "_official", "random_name", "priyanka", "sakhib"],
            random.randint(1, 3)
        )

        data[username] = {
            "username": username,
            "account_age_minutes": account_age,
            "followers_count": followers,
            "following_count": following,
            "posts_count": posts,
            "devices": devices,
            "locations": locations,
            "username_history": username_history
        }

    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)

    return data


def load_database():
    if not DB_PATH.exists():
        return create_random_database()

    with open(DB_PATH, "r") as f:
        return json.load(f)


def get_account(username):
    db = load_database()
    return db.get(username)