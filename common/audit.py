import os
import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "audit.log")

def log_action(action, user=None, filename=None, recognition_type=None, confidence=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Action: {action}"
    if user:
        entry += f", User: {user}"
    if filename:
        entry += f", File: {filename}"
    if recognition_type:
        entry += f", Type: {recognition_type}"
    if confidence is not None:
        entry += f", Confidence: {confidence:.2f}"
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
