from flask import Flask, jsonify, Response, send_from_directory, request
from flask_cors import CORS
from camera_service import generate_frames
from alert_service import AlertService
import threading
import time
import os
from sensor_service import SensorService
from history_service import HistoryService
from database import create_tables
from contact_service import ContactService
from telegram_service import TelegramService


app = Flask(
    __name__,
    static_folder="../web_app",
    static_url_path=""
)

CORS(app)
app = Flask(__name__)
CORS(app)
create_tables()

telegram_service = TelegramService()
alert_service = AlertService()
sensor_service = SensorService()
history_service = HistoryService()
contact_service = ContactService()
telegram_sent = False
monitoring_active = False

def format_status_history(status):

    if status == "fall_detected":
        return "Fall detected"

    if status == "possible_fall":
        return "Waiting for user confirmation"

    if status == "emergency_countdown":
        return "Emergency countdown started"

    if status == "emergency":
        return "Emergency message sent"

    return status

def simulation_loop():

    previous_status = None

    while True:

        global monitoring_active

        alert_service.update()

        if sensor_service.read_pir():

            monitoring_active = True

        else:

            monitoring_active = False

        current_status = alert_service.get_status()["status"]

        global telegram_sent

        if current_status == "emergency" and not telegram_sent:

            message = """
        🚨 EMERGENCY ALERT

        Possible fall detected.

        The user did not respond.

        Immediate assistance may be required.

        AIoT Emergency Detection System
        """

            contacts = contact_service.get_contacts()

            if len(contacts) > 0:

                message += "\n\nEmergency Contacts:\n"

                for contact in contacts:

                    message += (
                        f"\n{contact[1]}"
                        f" - "
                        f"{contact[2]}"
                    )

            telegram_service.send_message(message)

            telegram_sent = True

            print("TELEGRAM ALERT SENT")

        if current_status != previous_status:

            if current_status != "safe":
                history_service.add(
                    format_status_history(current_status)
                )

            previous_status = current_status

        time.sleep(1)

@app.route("/")
def home():

    web_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "web_app"
    )

    return send_from_directory(
        web_path,
        "index.html"
    )


## Pruebas de funcionalidades

@app.route("/test_history")
def test_history():

    history_service.add("Test Event")

    return jsonify({
        "message": "History test"
    })

@app.route("/test_fall")
def test_fall():

    alert_service.detect_possible_fall()

    history_service.add("Test Fall")

    return jsonify({
        "message": "Fall simulated"
    })

@app.route("/test_telegram")
def test_telegram():

    print("TEST ROUTE ENTERED")

    telegram_service.send_message(
        "Telegram test successful"
    )

    print("MESSAGE FUNCTION CALLED")

    return "ok"

## Fin de pruebas

## recursos

@app.route("/assets/<path:filename>")
def assets(filename):

    assets_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "web_app",
        "assets"
    )

    return send_from_directory(
        assets_path,
        filename
    )

## fin recursos

## Contactos
@app.route("/contacts")
def get_contacts():

    contacts = []

    rows = contact_service.get_contacts()

    for row in rows:

        contacts.append({

            "id": row[0],
            "name": row[1],
            "phone": row[2]

        })

    return jsonify(contacts)

@app.route(
    "/add_contact",
    methods=["POST"]
)
def add_contact():

    data = request.json

    contact_service.add_contact(

        data["name"],
        data["phone"]

    )

    return jsonify({
        "message": "Contact added"
    })

@app.route(
    "/delete_contact/<int:contact_id>"
)
def delete_contact(contact_id):

    contact_service.delete_contact(
        contact_id
    )

    return jsonify({
        "message": "Contact deleted"
    })

#Fin ruta contactos

@app.route("/simulate_fall")
def simulate_fall():

    global telegram_sent

    telegram_sent = False

    alert_service.detect_possible_fall()

    return jsonify({
        "message": "Possible fall triggered"
    })

@app.route("/test_buzzer")
def test_buzzer():

    sensor_service.beep(times=3)

    return jsonify({
        "message": "Buzzer test executed"
    })


@app.route("/user_ok")
def user_ok():

    global telegram_sent

    previous_status = alert_service.get_status()["status"]

    telegram_sent = False

    alert_service.user_is_ok()

    sensor_service.buzzer_off()

    history_service.add(
        "User Confirmed Safe"
    )

    if previous_status in [
        "fall_detected",
        "possible_fall",
        "emergency_countdown"
    ]:

        message = """
✅ FALSE ALARM

The user confirmed they are safe.

No emergency assistance is required.

AIoT Emergency Detection System
"""

        telegram_service.send_message(
            message
        )

        history_service.add(
            "False alarm message sent"
        )

    return jsonify({
        "message": "User confirmed okay"
    })

@app.route("/manual_emergency")
def manual_emergency():

    alert_service.manual_emergency()
    sensor_service.buzzer_on()
    history_service.add("Emergency Activated")

    return jsonify({
        "message": "Emergency manually triggered"
    })

@app.route("/status")
def status():
    return jsonify(alert_service.get_status())

@app.route("/ai_fall_trigger")
def ai_fall_trigger():

    global telegram_sent

    telegram_sent = False

    alert_service.detect_possible_fall()

    history_service.add("Fall Detected")

    return jsonify({
        "message": "AI fall trigger received"
    })

@app.route("/sensor_status")
def sensor_status():

    return jsonify(
        sensor_service.get_sensor_status()
    )

@app.route("/monitoring_status")
def monitoring_status():

    room_status = (
        "Occupied"
        if sensor_service.read_pir()
        else
        "No Occupancy Detected"
    )

    monitoring = (
        "Active"
        if monitoring_active
        else
        "Inactive"
    )

    return jsonify({

        "room_status": room_status,

        "monitoring": monitoring

    })

@app.route("/simulate_pir_on")
def simulate_pir_on():

    sensor_service.simulate_pir(True)

    return jsonify({
        "message": "PIR ON"
    })


@app.route("/simulate_pir_off")
def simulate_pir_off():

    sensor_service.simulate_pir(False)

    return jsonify({
        "message": "PIR OFF"
    })


@app.route("/simulate_sound/<int:value>")
def simulate_sound(value):

    sensor_service.simulate_sound(value)

    return jsonify({
        "message": f"Sound set to {value}"
    })


@app.route("/buzzer_on")
def buzzer_on():

    sensor_service.buzzer_on()

    return jsonify({
        "message": "Buzzer ON"
    })


@app.route("/buzzer_off")
def buzzer_off():

    sensor_service.buzzer_off()

    return jsonify({
        "message": "Buzzer OFF"
    })



@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/pose_test")
def pose_test():

    run_pose_detection()

    return jsonify({
        "message": "Pose detection finished"
    })

@app.route("/")
def index():
    return send_from_directory("../web_app", "index.html")

@app.route("/history")
def history():

    return jsonify(
        history_service.get_history()
    )

if __name__ == "__main__":
    simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
    simulation_thread.start()

    app.run(host="0.0.0.0", port=5000)