import requests
import os

ULTRAMSG_TOKEN = os.environ["ULTRAMSG_TOKEN"]
INSTANCE_ID = os.environ["INSTANCE_ID"]

url = f"https://api.ultramsg.com/{INSTANCE_ID}/messages/chat"

data = {
    "token": ULTRAMSG_TOKEN,
    "to": "919876543210",  # your test number in correct format
    "body": "Hello from GitHub Actions test!"
}

response = requests.post(url, data=data)
print(response.status_code)
print(response.text)
