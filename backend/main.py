from flask import Flask, jsonify, Response, send_from_directory
from flask_cors import CORS
from camera_service import generate_frames
from alert_service import AlertService
import threading
import time
import os

app = Flask(
    __name__,
    static_folder="../web_app",
    static_url_path=""
)

CORS(app)


app = Flask(__name__)
CORS(app)

alert_service = AlertService()

def simulation_loop():

    while True:

        if is_fall_detected():

            alert_service.trigger_possible_fall()

        alert_service.update()

        time.sleep(1)

@app.route("/")
def home():
    return "AIOT Emergency System Running"

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