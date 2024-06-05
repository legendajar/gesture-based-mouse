import mediapipe as mp
import util
import pyautogui
from pynput.mouse import Button, Controller
import cv2
import random

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode = False,
    model_complexity = 1,
    min_detection_confidence = 0.7,
    min_tracking_confidence = 0.7,
    max_num_hands = 1
)
def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        
        return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]

    return None 

def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x, y, duration=0.1)

def is_left_click(landmarks_list, thumb_index_dist):
    return(
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list [8]) < 50 and # for angle of index finger
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) > 90 and # for angle of middle finger
        thumb_index_dist > 50 # for angle between thumb and index finger
    )

def is_right_click(landmarks_list, thumb_index_dist):
    return(
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list [8]) > 90 and # for the angle of index finger
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and # for the angle of middle finger
        thumb_index_dist > 50 # for the angle between thumb and index finger
    )

def is_double_click(landmarks_list, thumb_index_dist):
    return(
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list [8]) < 50 and # for the angle of index finger 
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and # for the angle of middle finger
        thumb_index_dist > 50 # for the angle between thumb and index finger
    )
def is_screenshot(landmarks_list, thumb_index_dist):
    return(
        util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list [8]) <50 and # for the angle of index finger
        util.get_angle(landmarks_list[9], landmarks_list[10], landmarks_list[12]) < 50 and # for the angle of middle finger
        thumb_index_dist < 50 # for the angle between thumb and index finger
    )

def is_volume(landmarks_list):
    return(
        util.get_angle(landmarks_list[4], landmarks_list[2], landmarks_list[1]) > 90 and
        util.get_angle(landmarks_list[8], landmarks_list[6], landmarks_list[5]) > 90 and 
        util.get_angle(landmarks_list[12], landmarks_list[10], landmarks_list[9]) < 50 and 
        util.get_distance(landmarks_list)
    )


def is_zoom(landmarks_list, thumb_index_dist):
    pass


def detect_gesture(frame, landmarks_list, processed):
    if len(landmarks_list) >= 21:
        
        # Movement of the mouse pointer
        index_finger_tip = find_finger_tip(processed)

        # Here we are finding the thumb distance because the pointer will move only when the thumb is down and only index finger is up. To find whether the thumb is up or down we need to calculate the distance between point 4 and point 5. If it is zero, then thumb is down else thumb is up

        thumb_index_distance = util.get_distance([landmarks_list[4], landmarks_list[5]])
        index_angle = util.get_angle(landmarks_list[5], landmarks_list[6], landmarks_list[8])


        # MOUSE MOVE
        if thumb_index_distance < 50 and index_angle > 90:
            move_mouse(index_finger_tip)
        
        # LEFT CLICK
        elif is_left_click(landmarks_list, thumb_index_distance):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame,"Left Click", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2 )
        
        # RIGHT CLICK
        elif is_right_click(landmarks_list, thumb_index_distance):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame,"Right Click", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2 )

        # DOUBLE CLICK
        elif is_double_click(landmarks_list, thumb_index_distance):
            pyautogui.doubleClick()
            cv2.putText(frame,"Double Click", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2 )
            
        # SCREENSHOT
        elif is_screenshot(landmarks_list, thumb_index_distance):
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            im1.save(f'/home/legendajar/Desktop/new-projects/gesture-based-mouse/ss/my_screenshot_${label}.png')
            cv2.putText(frame,"Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2 )

        # VOLUME
        elif is_volume(landmarks_list):
            cv2.putText(frame,"Volume", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2 )