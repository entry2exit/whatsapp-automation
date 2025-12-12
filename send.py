import csv
import json
import time
import requests

ULTRAMSG_TOKEN = "REPLACE_WITH_YOUR_TOKEN"
INSTANCE_ID = "REPLACE_WITH_YOUR_INSTANCE"

BATCH_SIZE = 300  # messages per day
MESSAGE_TEXT = "Hello! This is your automated update."

# 1. Load state
with open("state.json") as f:
    state = json.load(f)

last_index = state["last_index"]

# 2. Load contacts
contacts = []
with open("contacts.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        contacts.append(row)

# 3. Determine batch
start = last_index
end = min(last_index + BATCH_SIZE, len(contacts))

batch = contacts[start:end]

# 4. Send messages
for person in batch:
    payload = {
        "token": ULTRAMSG_TOKEN,
        "to": person["phone"],
        "body": MESSAGE_TEXT
    }
    
    url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"
    try:
        requests.post(url, data=payload)
        time.sleep(0.2)  # 200ms between messages
    except:
        pass  # ignore failures for now

# 5. Update state
new_index = end if end < len(contacts) else 0
state["last_index"] = new_index

# 6. Save updated state
with open("state.json", "w") as f:
    json.dump(state, f, indent=2)
