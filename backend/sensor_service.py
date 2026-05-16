from config import RUN_MODE

class SensorService:
    def __init__(self):
        self.pir_detected = False
        self.sound_detected = False

    def read_pir(self):
        if RUN_MODE == "SIMULATION":
            return self.pir_detected

    def read_sound(self):
        if RUN_MODE == "SIMULATION":
            return self.sound_detected

    def simulate_pir(self, state):
        self.pir_detected = state

    def simulate_sound(self, state):
        self.sound_detected = state