import cv2
import mediapipe as mp
import requests
import time

RASPBERRY_URL = "http://192.168.0.132:5000/ai_fall_trigger"

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

camera = cv2.VideoCapture(
    "http://192.168.0.132:5000/video_feed"
)

fall_detected = False
last_trigger_time = 0

while True:

    success, frame = camera.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    if results.pose_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        shoulder_y = (
            left_shoulder.y +
            right_shoulder.y
        ) / 2

        hip_y = (
            left_hip.y +
            right_hip.y
        ) / 2

        body_height = abs(hip_y - shoulder_y)

        shoulder_width = abs(
            left_shoulder.x -
            right_shoulder.x
        )

        # Detectar postura horizontal
        if body_height < 0.18 and shoulder_width > 0.15:

            cv2.putText(
                frame,
                "POSSIBLE FALL",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

            current_time = time.time()

            if current_time - last_trigger_time > 10:

                try:

                    requests.get(RASPBERRY_URL)

                    print("AI FALL TRIGGER SENT")

                    last_trigger_time = current_time

                except:
                    print("Could not connect to Raspberry")

    cv2.imshow(
        "AI Fall Detection",
        frame
    )

    key = cv2.waitKey(1)

    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()