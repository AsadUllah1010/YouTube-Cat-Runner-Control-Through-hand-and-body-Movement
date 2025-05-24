import cv2
import mediapipe as mp
import pyautogui
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_action_time = time.time()

def count_fingers(hand_landmarks):
    fingers = []
    tip_ids = [4, 8, 12, 16, 20]

    # Thumb
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers (index to pinky)
    for id in range(1, 5):
        if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            finger_count = count_fingers(handLms)
            current_time = time.time()

            # Limit actions to once per second
            if current_time - prev_action_time > 1:
                if finger_count == 0:
                    pyautogui.press('space')  # Play/Pause
                    print("Play/Pause")
                elif finger_count == 1:
                    pyautogui.press('down')  # Volume Down
                    print("Volume Down")
                elif finger_count == 2:
                    pyautogui.press('up')    # Volume Up
                    print("Volume Up")
                elif finger_count == 3:
                    pyautogui.press('left')  # Rewind
                    print("Rewind")
                elif finger_count == 4:
                    pyautogui.press('right') # Forward
                    print("Forward")
                elif finger_count == 5:
                    pyautogui.press('f')     # Fullscreen toggle
                    print("Fullscreen Toggle")
                
                prev_action_time = current_time

    cv2.imshow("Hand Control for YouTube", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
