import requests


class TelegramService:

    def __init__(self):

        self.bot_token = "8641624677:AAGGUtAxMJljc2dWaheUQ-O6zyyMKxy_hbI"

        self.chat_id = "8903958713"


    def send_message(self, message):

        print("SEND MESSAGE STARTED")

        url = (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}/sendMessage"
        )

        response = requests.post(
            url,
            json={
                "chat_id": self.chat_id,
                "text": message
            }
        )

        print(response.text)