from config import RUN_MODE, PIR_PIN, BUZZER_PIN, SOUND_CHANNEL, SOUND_THRESHOLD
import time


class SensorService:

    def __init__(self):

        self.simulated_pir = False
        self.simulated_sound_value = 0
        self.simulated_buzzer = False

        if RUN_MODE == "RASPBERRY":
            self.setup_raspberry()

    def setup_raspberry(self):

        try:

            from gpiozero import MotionSensor, Buzzer

            self.pir = MotionSensor(PIR_PIN)

            self.buzzer = Buzzer(BUZZER_PIN)

            print("GPIOZERO initialized")

        except Exception as e:

            print("GPIO setup error:", e)

    def read_pir(self):

        if RUN_MODE == "SIMULATION":
            return self.simulated_pir

        return self.pir.motion_detected

    def read_sound(self):

        if RUN_MODE == "SIMULATION":
            return self.simulated_sound_value

        return 0

    def is_loud_sound(self):

        return self.read_sound() >= SOUND_THRESHOLD

    def buzzer_on(self):

        if RUN_MODE == "SIMULATION":

            self.simulated_buzzer = True

            print("BUZZER ON (simulation)")

            return

        self.buzzer.on()

        print("BUZZER ON")

    def buzzer_off(self):

        if RUN_MODE == "SIMULATION":

            self.simulated_buzzer = False

            print("BUZZER OFF (simulation)")

            return

        self.buzzer.off()

        print("BUZZER OFF")

    def beep(self, duration=0.25, times=1, pause=0.15):

        print(f"BUZZER BEEP x{times}")

        for _ in range(times):

            self.buzzer_on()

            time.sleep(duration)

            self.buzzer_off()

            time.sleep(pause)

    def simulate_pir(self, state):

        self.simulated_pir = state

    def simulate_sound(self, value):

        self.simulated_sound_value = value

    def get_sensor_status(self):

        return {
            "pir_detected": self.read_pir(),
            "sound_value": self.read_sound(),
            "loud_sound": self.is_loud_sound(),
            "buzzer": self.simulated_buzzer
        }

    def cleanup(self):

        if RUN_MODE == "RASPBERRY":

            self.buzzer.off()