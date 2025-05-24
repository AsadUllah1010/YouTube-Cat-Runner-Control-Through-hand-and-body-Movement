import cv2
import mediapipe as mp
import pyautogui
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
height_threshold = 300  # Adjust based on your camera setup
center_x = 320  # Assuming 640px width
jumped = slid = moved_left = moved_right = False

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Key points
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # Movement detection
        if nose.y < 0.4 and not jumped:
            pyautogui.press('up')
            jumped = True
        elif nose.y >= 0.4:
            jumped = False

        if nose.y > 0.6 and not slid:
            pyautogui.press('down')
            slid = True
        elif nose.y <= 0.6:
            slid = False

        if nose.x < 0.4 and not moved_left:
            pyautogui.press('left')
            moved_left = True
        elif nose.x >= 0.4:
            moved_left = False

        if nose.x > 0.6 and not moved_right:
            pyautogui.press('right')
            moved_right = True
        elif nose.x <= 0.6:
            moved_right = False

        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('Game Controller - Move to Play!', frame)

    if cv2.waitKey(5) & 0xFF == 27:  # Press Esc to quit
        break

cap.release()
cv2.destroyAllWindows()

