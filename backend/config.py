# =========================
# PROJECT CONFIGURATION
# =========================

# Cambiar a "RASPBERRY" cuando el proyecto esté en la Raspberry Pi
RUN_MODE = "SIMULATION"

# GPIO pins for Raspberry Pi
PIR_PIN = 17
SOUND_PIN = 27
BUZZER_PIN = 22

# Emergency timing
FALL_CONFIRMATION_SECONDS = 120
USER_RESPONSE_SECONDS = 120