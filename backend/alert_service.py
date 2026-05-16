import time

class AlertService:

    def __init__(self):

        self.status = "safe"

        self.fall_detected_time = None

        self.emergency_sent = False
        self.history = []

    # -------------------------
    # DETECT FALL
    # -------------------------

    def detect_possible_fall(self):

        print("Possible fall detected.")
        self.history.append("Possible fall detected")

        self.status = "possible_fall"

        self.fall_detected_time = time.time()

        self.emergency_sent = False

    # -------------------------
    # USER CONFIRMS OKAY
    # -------------------------

    def user_is_ok(self):

        print("User confirmed: I am okay.")
        self.history.append("User confirmed: I am okay.")

        self.status = "safe"

        self.fall_detected_time = None

        self.emergency_sent = False

    # -------------------------
    # MANUAL EMERGENCY BUTTON
    # -------------------------

    def manual_emergency(self):

        print("MANUAL EMERGENCY ACTIVATED")

        self.status = "emergency"

        self.emergency_sent = True

    # -------------------------
    # AUTO UPDATE LOOP
    # -------------------------

    def update(self):

        if self.status == "possible_fall":

            elapsed = time.time() - self.fall_detected_time

            print(f"Waiting confirmation... {int(elapsed)} sec")

            # 20 segundos para pruebas
            if elapsed >= 20 and not self.emergency_sent:

                self.trigger_emergency()

    # -------------------------
    # TRIGGER EMERGENCY
    # -------------------------

    def trigger_emergency(self):

        print("EMERGENCY SENT TO CONTACTS")
        self.history.append("Emergency sent to contacts")

        self.status = "emergency"

        self.emergency_sent = True

    # -------------------------
    # GET STATUS
    # -------------------------

    def get_status(self):

        return {
         "status": self.status,
         "history": self.history[-10:]
        }