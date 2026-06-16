##from picamera2 import Picamera2

import cv2

camera = cv2.VideoCapture(0)

##picam2 = Picamera2()
## picam2.configure(
##    picam2.create_video_configuration(
##        main={"size": (640, 480), "format": "RGB888"}
##    )
##)
##picam2.start()
def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            continue

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes() +
            b"\r\n"
        )

