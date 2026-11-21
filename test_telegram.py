import requests


BOT_TOKEN = '9107666693:AAEzXBnYQy2AqGZp4n4NCTJjnETjyV6kUfE'
CHAT_ID = '672196988'

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": "Hello From Python! Test IT JOB ALERTS"
}

response = requests.post(url, payload, timeout=15)

response.raise_for_status()

data = response.json()

print("Sent successfully! Message ID:", data["result"]["message_id"])



