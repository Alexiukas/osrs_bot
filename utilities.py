import os
import random
import time
import cv2 as cv
import mss
import pyautogui
import win32gui
from dictionary import game_screen

font = cv.FONT_HERSHEY_SIMPLEX
DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def get_osrs_coordinates():
    window = win32gui.FindWindow(None, "Old School Runescape")
    if window == 0:
        return window
    game_coordinates = list(win32gui.GetWindowRect(window))

    if game_coordinates[0] < 0 and game_coordinates[2] < 0:
        return 0

    return game_coordinates


def take_picture(save=True, full_client=False, screen=None, name="test.png"):
    coordinates = get_osrs_coordinates()

    if full_client is False and screen is None:
        print("Screen has no coordinates")
        return

    with mss.mss() as sct:
        monitor = {"left": coordinates[0] + (0 if full_client else screen[0]),
                   "top": coordinates[1] + (0 if full_client else screen[1]),
                   "width": coordinates[2] - coordinates[0] if full_client else screen[2],
                   "height": coordinates[3] - coordinates[1] if full_client else screen[3]}
        ss = sct.grab(monitor)
        if save:
            mss.tools.to_png(ss.rgb, ss.size, output=os.path.join(os.path.dirname(os.path.realpath(__file__)), name))
        return ss


def setup_rs_client(mouse_mover, zoomed_in=False, resizable=False):
    game_coordinates = get_osrs_coordinates()
    if game_coordinates == 0:
        return
    x, y = pyautogui.position()
    mouse_mover.wind_mouse(x, y, game_coordinates[2] - 1, game_coordinates[3] - 1, click=False)
    mouse_mover.wind_mouse(game_coordinates[2] - 1, game_coordinates[3] - 1, game_coordinates[0] + (947 + 15 if resizable else 783),
                           game_coordinates[1] + (561 + 37 if resizable else 603), click=False, drag=True)

    filter_pos = [80, 515, 125, 530]
    select_filter_pos = [52, 488, 126, 498]
    options_pos = [683, 505, 700, 525]
    sun_pos = [717, 309, 719, 313]
    zoom_pos = [652, 346, 670, 351] if zoomed_in else [638, 346, 643, 351]

    time.sleep(0.5)
    x, y = pyautogui.position()
    mouse_mover.wind_mouse(x, y, game_coordinates[0] + random.randint(options_pos[0], options_pos[2]), game_coordinates[1] + random.randint(options_pos[1], options_pos[3]))
    time.sleep(0.5)
    x, y = pyautogui.position()
    mouse_mover.wind_mouse(x, y, game_coordinates[0] + random.randint(sun_pos[0], sun_pos[2]), game_coordinates[1] + random.randint(sun_pos[1], sun_pos[3]))
    time.sleep(0.5)
    x, y = pyautogui.position()
    mouse_mover.wind_mouse(x, y, game_coordinates[0] + random.randint(zoom_pos[0], zoom_pos[2]), game_coordinates[1] + random.randint(zoom_pos[1], zoom_pos[3]))
    time.sleep(0.5)
    x, y = pyautogui.position()
    mouse_mover.wind_mouse(x, y, game_coordinates[0] + random.randint(filter_pos[0], filter_pos[2]), game_coordinates[1] + random.randint(filter_pos[1], filter_pos[3]), click=False)
    pyautogui.rightClick()
    time.sleep(0.5)
    x, y = pyautogui.position()
    mouse_mover.wind_mouse(x, y, game_coordinates[0] + random.randint(select_filter_pos[0], select_filter_pos[2]), game_coordinates[1] + random.randint(select_filter_pos[1], select_filter_pos[3]))
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')


def draw_bb(pic, predictions, client):
    img = cv.imread(pic)
    window = cv.namedWindow('bounding boxes')

    if client == 0:
        raise TypeError("Client variable must be a list")

    cv.moveWindow('bounding boxes', client[2], client[3])
    for prediction in predictions:
        x1 = int(prediction['x'] - prediction['width'] / 2)
        x2 = int(prediction['x'] + prediction['width'] / 2)
        y1 = int(prediction['y'] - prediction['height'] / 2)
        y2 = int(prediction['y'] + prediction['height'] / 2)

        cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        cv.putText(img, 'OpenCV', (x1 + 5, y1 + 5), font, 4, (255, 255, 255), 1, cv.LINE_AA)

    cv.imshow('bounding boxes', img)


def move_mouse(mouse, target_x, target_y, click=True, drag=False):
    client_pos = get_osrs_coordinates()
    mouse_x, mouse_y = pyautogui.position()
    mouse.wind_mouse(mouse_x, mouse_y, client_pos[0] + target_x, client_pos[1] + target_y, click=click, drag=drag)


if __name__ == "__main__":
    pass
