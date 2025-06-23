import datetime
import os

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "fake_blockchain_log.txt"))
print("🛠️ Salvare log în:", LOG_PATH)

def log_event(patient_id, event_type):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"{timestamp} - {patient_id} - {event_type}\n")
    print(f"⛓️ [Simulat] Log: {timestamp} - {patient_id} - {event_type}")
