import datetime
import os
import random
import time
import cv2 as cv
import numpy as np
import pyautogui
from roboflow import Roboflow
import dictionary
import utilities
import object_detector
from utilities import move_mouse
import file_worker


rf = Roboflow(api_key="yIAp6vCfMnEWvjbsTyLl")
project = rf.workspace().project("osrs-trees-f2p")
model = project.version(1).model
FILE_PATH = os.path.dirname(os.path.realpath(__file__))


class GatheringBot:
    def __init__(self, logs, script, running, stop, paused, loot, mouse):
        self.log_msg = logs
        self.stop = stop
        self.paused = paused
        self.loot_count = loot
        self.mouse = mouse()
        self.script = script
        self.running = running
        self.full_action = self.script['action']
        self.action = self.full_action[self.full_action.index(' '):].lower().strip()

    def run(self):
        bot_type = self.script["bot_type"]
        start, date = time.time(), datetime.datetime.now()
        wc = True if "Woodcutting" in self.script["name"] else False
        file_worker.load_templates(file_worker.PATH_TO_ITEMS)

        self.log_msg("Setting up client..")
        utilities.setup_rs_client(mouse_mover=self.mouse, zoomed_in=True if bot_type == 'color' else False)

        while self.running():
            if self.paused():
                time.sleep(1)
                continue

            if time.time() - start > self.script["run_time"] * 60:
                self.log_msg("Script run time finished. Stopping..")
                self.stop()
                break

            screenshot = utilities.take_picture(True, False, dictionary.game_screen, "bot_running.png")
            self.log_msg("Trying to detect objects")

            if bot_type == 'roboflow' and not self.roboflow_logic():
                continue

            inventory = object_detector.match_templates(self.action)

            if bot_type == 'color' and not self.color_logic(screenshot):
                continue

            time.sleep(2.5)

            if is_inventory_full(not wc):
                self.drop_items(inventory)
                if wc:
                    pyautogui.write("s")
                    pyautogui.press("enter")
                continue

            start_inv_size = len(inventory)

            if bot_type != 'local':
                self.check_for_loot(start_inv_size, wc)

        if not self.running():
            self.log_msg("User stopped the script.")

    def drop_items(self, items):
        pyautogui.keyDown("shift")
        for item in items:
            if not self.running() and self.paused():
                return
            item_x = random.randint(item[0][0], item[1][0])
            item_y = random.randint(item[0][1], item[1][1])
            utilities.move_mouse(self.mouse, item_x + dictionary.bag_screen[0], item_y + dictionary.bag_screen[1])
            time.sleep(random.uniform(0.1, 0.2))
        pyautogui.keyUp("shift")

    def roboflow_logic(self):
        predictions = model.predict(FILE_PATH + "\\bot_running.png", confidence=80, overlap=30).json()["predictions"]

        if len(predictions) == 0:
            self.log_msg("No predictions have been made. Waiting for 5 seconds to try again..")
            time.sleep(5)
            return False
        else:
            for prediction in predictions:
                if prediction["class"].lower() == self.action.lower():
                    self.log_msg("Trying to " + self.full_action)
                    move_mouse(self.mouse, prediction['x'] + dictionary.game_screen[0], prediction['y'] + dictionary.game_screen[0])
                    return True
            self.log_msg("Can't find needed object..")
            time.sleep(5)
            return False

    def color_logic(self, screenshot):
        location = object_detector.get_pixel_location(screenshot, dictionary.fishing_spot_lower, dictionary.fishing_spot_upper)

        if location is None:
            self.log_msg("No predictions have been made. Waiting for 5 seconds to try again..")
            time.sleep(5)
            return False

        self.log_msg("Trying to " + self.full_action)
        utilities.move_mouse(self.mouse, location[0] + dictionary.game_screen[0], location[1] + dictionary.game_screen[1])
        return True

    def check_for_loot(self, start_inv_size, wc):
        time_to_check = time.time()
        while True and self.running() and not self.paused():
            time.sleep(0.5)
            inventory = object_detector.match_templates(self.action)
            inv_size = len(inventory)

            if is_inventory_full(not wc):
                self.drop_items(inventory)
                return

            if start_inv_size == inv_size - 1:
                self.log_msg("Got +1 " + self.action)
                self.loot_count.set(self.loot_count.get() + 1)
                start_inv_size = inv_size

                if not self.script['wait']:
                    return
                time_to_check = time.time()

            if time.time() - time_to_check > 15:
                self.log_msg("Didn't collect anything for a while..")
                return


def is_inventory_full(blue=True):
    img = np.array(utilities.take_picture(False, False, dictionary.full_inv_screen if blue else dictionary.full_inv_wc))
    img = cv.cvtColor(cv.cvtColor(img, cv.COLOR_RGB2BGR), cv.COLOR_BGR2RGB)
    color = (255, 0, 0) if blue else (0, 0, 0)
    mask = cv.inRange(img, color, color)
    pixels = cv.countNonZero(mask)
    return pixels > 250 if blue else 268 < pixels < 272


if __name__ == "__main__":
    pass
