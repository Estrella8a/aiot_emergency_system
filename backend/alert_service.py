import time

class AlertService:

    def __init__(self):
        self.status = "safe"
        self.fall_detected_time = None
        self.user_alert_time = None
        self.emergency_countdown_time = None
        self.emergency_sent = False
        self.history = []

        self.FALL_CONFIRMATION_SECONDS = 10
        self.USER_RESPONSE_SECONDS = 20
        self.EMERGENCY_SEND_SECONDS = 10

    def detect_possible_fall(self):

        if self.status == "safe":
            print("Fall detected. Waiting confirmation...")
            self.status = "fall_detected"
            self.fall_detected_time = time.time()
            self.history.append("Fall detected by AI")

    def update(self):

        now = time.time()

        if self.status == "fall_detected":
            elapsed = now - self.fall_detected_time

            if elapsed >= self.FALL_CONFIRMATION_SECONDS:
                self.status = "possible_fall"
                self.user_alert_time = now
                self.history.append("Are you okay? alert shown")
                print("Are you okay?")

        elif self.status == "possible_fall":
            elapsed = now - self.user_alert_time

            if elapsed >= self.USER_RESPONSE_SECONDS:
                self.status = "emergency_countdown"
                self.emergency_countdown_time = now
                self.history.append("Emergency countdown started")
                print("Emergency countdown started")

        elif self.status == "emergency_countdown":
            elapsed = now - self.emergency_countdown_time

            if elapsed >= self.EMERGENCY_SEND_SECONDS:
                self.status = "emergency"
                self.emergency_sent = True
                self.history.append("Emergency message sent to contacts")
                print("Emergency message sent to contacts")

    def user_is_ok(self):
        print("User confirmed okay")

        self.status = "safe"
        self.fall_detected_time = None
        self.user_alert_time = None
        self.emergency_countdown_time = None
        self.emergency_sent = False

        self.history.append("User confirmed: I'm okay")

    def manual_emergency(self):
        print("Manual emergency activated")

        self.status = "emergency"
        self.emergency_sent = True
        self.history.append("Manual emergency activated")

    def get_status(self):

        message = ""

        if self.status == "safe":
            message = "Safe"

        elif self.status == "fall_detected":
            message = "Fall detected. Confirming..."

        elif self.status == "possible_fall":
            message = "Are you okay?"

        elif self.status == "emergency_countdown":
            message = "Emergency will be sent soon..."

        elif self.status == "emergency":
            message = "Emergency sent to contacts"

        return {
            "status": self.status,
            "message": message,
            "emergency_sent": self.emergency_sent,
            "history": self.history[-10:]
        }