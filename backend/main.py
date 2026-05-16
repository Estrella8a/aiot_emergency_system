from flask import Flask, jsonify, Response, send_from_directory
from flask_cors import CORS
from camera_service import generate_frames
from alert_service import AlertService
import threading
import time
from flask import send_from_directory
import os
from sensor_service import SensorService
from emergency_engine import EmergencyEngine
#from fall_detection import is_fall_detected
#from fall_detection import run_pose_detection

app = Flask(
    __name__,
    static_folder="../web_app",
    static_url_path=""
)

CORS(app)


app = Flask(__name__)
CORS(app)

alert_service = AlertService()
sensor_service = SensorService()
emergency_engine = EmergencyEngine(alert_service, sensor_service)

def simulation_loop():

    while True:
        camera_fall = False

        emergency_engine.update(camera_fall)

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

@app.route("/simulate_fall")
def simulate_fall():
    alert_service.detect_possible_fall()
    return jsonify({"message": "Possible fall triggered"})

@app.route("/user_ok")
def user_ok():
    alert_service.user_is_ok()
    return jsonify({"message": "User confirmed okay"})

@app.route("/manual_emergency")
def manual_emergency():
    alert_service.manual_emergency()
    return jsonify({"message": "Emergency manually triggered"})

@app.route("/status")
def status():
    return jsonify(alert_service.get_status())

@app.route("/sensor_status")
def sensor_status():

    return jsonify(
        sensor_service.get_sensor_status()
    )


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

if __name__ == "__main__":
    simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
    simulation_thread.start()

    app.run(host="0.0.0.0", port=5000)