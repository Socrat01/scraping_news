import requests
from config import BOT_TOKEN, CHANNEL_ID

def send_telegram(message):

        url = "https://api.telegram.org/bot"
        channel_id = CHANNEL_ID
        url += BOT_TOKEN
        method = url + "/sendMessage"

        requests.post(method, data={
            "chat_id": channel_id,
            "text": message
        })