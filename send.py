import csv
import json
import os
import requests
from pathlib import Path

# ------------------------------------------------------------
# Load UltraMsg credentials from GitHub Secrets
# ------------------------------------------------------------
try:
    ULTRAMSG_TOKEN = os.environ["ULTRAMSG_TOKEN"]
    INSTANCE_ID = os.environ["INSTANCE_ID"]
except KeyError as e:
    print(f"Missing environment variable: {e}")
    exit(1)

API_URL = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

# ------------------------------------------------------------
# File paths
# ------------------------------------------------------------
CONTACTS_FILE = "contacts.csv"
STATE_FILE = "state.json"

# ------------------------------------------------------------
# Load contacts
# ------------------------------------------------------------
if not Path(CONTACTS_FILE).is_file():
    print("ERROR: contacts.csv not found.")
    exit(1)

contacts = []
with open(CONTACTS_FILE, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row and row[0]:
            phone = row[0].strip().replace("+", "").replace(" ", "")
            contacts.append(phone)

if not contacts:
    print("ERROR: contacts.csv has no numbers.")
    exit(1)

# ------------------------------------------------------------
# Load state.json
# ------------------------------------------------------------
if not Path(STATE_FILE).is_file():
    state = {"last_sent_index": -1}
else:
    with open(STATE_FILE, "r") as f:
        state = json.load(f)

last_index = state.get("last_sent_index", -1)
next_index = last_index + 1

# Reset logic (optional)
if next_index >= len(contacts):
    print("Reached end of contacts. Resetting to start.")
    next_index = 0

# ------------------------------------------------------------
# Sending logic
# ------------------------------------------------------------
phone_to_send = contacts[next_index]
message_text = "Hello! This is an automated WhatsApp message sent via GitHub Actions + UltraMsg."

payload = {
    "token": ULTRAMSG_TOKEN,
    "to": phone_to_send,
    "body": message_text
}

print(f"Sending to {phone_to_send} ...")

response = requests.post(API_URL, data=payload)

# Print UltraMsg response for debugging
print("Status Code:", response.status_code)
print("Response:", response.text)

# ------------------------------------------------------------
# Update state.json only if success
# ------------------------------------------------------------
try:
    resp_json = response.json()
    if resp_json.get("sent") or resp_json.get("id"):
        state["last_sent_index"] = next_index
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
        print(f"Message sent successfully. Updated state to index {next_index}.")
    else:
        print("Message not sent. UltraMsg returned an error.")
except ValueError:
    print("Invalid JSON response from UltraMsg. Not updating state.")
