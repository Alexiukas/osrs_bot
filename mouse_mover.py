import random
import time

import pyautogui
import numpy as np

sqrt3 = np.sqrt(3)
sqrt5 = np.sqrt(5)

pyautogui.MINIMUM_DURATION = 0
pyautogui.PAUSE = 0.01
pyautogui.MINIMUM_SLEEP = 0
compass_x = [780, 810]
compass_y = [37, 67]
start_x = [390, 440]
start_y = [120, 150]
_miss_click_chance = 0.1


def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=5, W_0=6, M_0=20, click=True, drag=False, D_0=15,
               move_mouse=lambda x, y: pyautogui.moveTo(x, y)):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational force
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    '''
    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    if drag:
        pyautogui.mouseDown()
    start_time = time.time()
    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1 and start_time - time.time() < 10:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random() * 3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0 * (dest_x - start_x) / dist
        v_y += W_y + G_0 * (dest_y - start_y) / dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0 / 2 + np.random.random() * M_0 / 2
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))

        if current_x != move_x or current_y != move_y:
            # This should wait for the mouse polling interval
            move_mouse(current_x := move_x, current_y := move_y)
    if click:
        pyautogui.click()
    if drag:
        pyautogui.mouseUp()
    return current_x, current_y
