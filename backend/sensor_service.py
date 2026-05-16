from config import RUN_MODE, PIR_PIN, BUZZER_PIN, SOUND_CHANNEL, SOUND_THRESHOLD


class SensorService:

    def __init__(self):
        self.simulated_pir = False
        self.simulated_sound_value = 0
        self.simulated_buzzer = False

        if RUN_MODE == "RASPBERRY":
            self.setup_raspberry()

    def setup_raspberry(self):
        try:
            import RPi.GPIO as GPIO

            self.GPIO = GPIO
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(PIR_PIN, GPIO.IN)
            GPIO.setup(BUZZER_PIN, GPIO.OUT)

            print("GPIO initialized")

        except Exception as e:
            print("GPIO setup error:", e)

    def read_pir(self):
        if RUN_MODE == "SIMULATION":
            return self.simulated_pir

        return self.GPIO.input(PIR_PIN) == 1

    def read_sound(self):
        if RUN_MODE == "SIMULATION":
            return self.simulated_sound_value

        # Aquí después leeremos el ADC real
        # Por ahora devuelve 0 para no romper el sistema
        return 0

    def is_loud_sound(self):
        return self.read_sound() >= SOUND_THRESHOLD

    def buzzer_on(self):
        if RUN_MODE == "SIMULATION":
            self.simulated_buzzer = True
            print("BUZZER ON (simulation)")
            return

        self.GPIO.output(BUZZER_PIN, self.GPIO.HIGH)

    def buzzer_off(self):
        if RUN_MODE == "SIMULATION":
            self.simulated_buzzer = False
            print("BUZZER OFF (simulation)")
            return

        self.GPIO.output(BUZZER_PIN, self.GPIO.LOW)

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