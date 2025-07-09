# src/story_counter.py

import json
import os

COUNTER_FILE = os.path.join("data", "story_count.json")

def get_next_story_id():
    """Load and increment story counter, save, and return new story ID"""
    count = 0

    # Make sure data folder exists
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)

    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            data = json.load(f)
            count = data.get("count", 0)

    count += 1

    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

    return count
