import requests
from time import sleep, strftime, localtime
from os import getenv
from dotenv import load_dotenv

# Get env variables
load_dotenv()
MODULE = getenv("MODULE")
COOKIE = getenv("COOKIE")
MAX_STUDENT = int(getenv("MAX_STUDENT"))
INTERVAL = int(getenv("INTERVAL"))
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
TELEGRAM_USERNAME = getenv("TELEGRAM_USERNAME")

# Get telegram chat id
chat_id = None

for update in requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates").json()["result"]:
  if "message" in update and update["message"]["chat"]["username"] == TELEGRAM_USERNAME:
    chat_id = update["message"]["chat"]["id"]

if chat_id is None:
  bot_name = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe').json()['result']['username']

  print(f"Envoie un message à ton bot pour qu'il puisse trouver la conversation: https://t.me/{bot_name}")
  exit(0)

# Start monitoring intra module
print("Début de la surveillance...")
while True:
  r = len(requests.get(
    f"https://intra.epitech.eu/module/{MODULE}/registered?format=json",
    headers={ "Cookie": COOKIE }
  ).json())
  print(f"{strftime('%H:%M:%S', localtime())} - {r}/{MAX_STUDENT} inscrits")

  if r != MAX_STUDENT:
    requests.post(
      f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
      json={
        "chat_id": chat_id,
        "text": f"🚨 Places dispos dans le [module](https://intra.epitech.eu/module/{MODULE}/) 🚨 {r}/{MAX_STUDENT} étudiants y sont inscrits",
        "parse_mode": "Markdown"
      }
    )
  sleep(INTERVAL)
