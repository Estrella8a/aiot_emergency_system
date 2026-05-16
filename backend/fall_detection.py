import cv2
import mediapipe as mp
import math

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

fall_detected = False

def draw_pose(frame):

    global fall_detected

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    fall_detected = False

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        x1 = left_shoulder.x
        y1 = left_shoulder.y

        x2 = right_shoulder.x
        y2 = right_shoulder.y

        angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))

        if angle < 20:
            fall_detected = True

            cv2.putText(
                frame,
                "POSSIBLE FALL",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    return frame


def is_fall_detected():
    return fall_detected