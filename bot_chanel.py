import requests
from config import BOT_TOKEN

def send_telegram(message):

        url = "https://api.telegram.org/bot"
        channel_id = "@tesmanian_news"
        url += BOT_TOKEN
        method = url + "/sendMessage"

        requests.post(method, data={
            "chat_id": channel_id,
            "text": message
        })