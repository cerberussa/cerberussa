import json
from datetime import datetime
import os

LOG_FILE = "bookings_log.json"

def log_booking(service, booking_data):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "service": service,
        "data": booking_data
    }
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                all_bookings = json.load(f)
        else:
            all_bookings = []

        all_bookings.append(record)

        with open(LOG_FILE, "w") as f:
            json.dump(all_bookings, f, indent=2)

    except Exception as e:
        print("Logging failed:", e)