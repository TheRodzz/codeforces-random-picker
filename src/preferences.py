import json
import os

def load_preferences():
    try:
        with open("preferences.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_preferences(preferences):
    with open("preferences.json", "w") as f:
        json.dump(preferences, f)

def load_bookmarks():
    try:
        with open("bookmarks.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_bookmarks(bookmarks):
    with open("bookmarks.json", "w") as f:
        json.dump(bookmarks, f)