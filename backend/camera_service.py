import cv2
from fall_detection import draw_pose

camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()

        if not success:
            break

        
        ## frame = draw_pose(frame)

        ret, buffer = cv2.imencode(".jpg", frame)

        if not ret:
            continue

        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
        )