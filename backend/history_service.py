from datetime import datetime


class HistoryService:

    def __init__(self):
        self.events = []

    def add(self, event):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.events.insert(0, {
            "time": timestamp,
            "event": event
        })

        self.events = self.events[:20]

    def get_history(self):
        return self.events