import random
import torch
import os
import numpy as np
import file_worker
import utilities
import dictionary
import pyautogui
import time
import object_detector


class CombatBot:
    def __init__(self, logs, script, stop, was_stopped, pause, kc, mouse_settings):
        self.log_msg = logs
        self.script_info = script
        self.running = True
        self.pause = pause
        self.kill_count = kc
        self.was_stopped = was_stopped
        self.stop = stop
        self.is_in_combat = False
        self.index = 0
        self.mouse = mouse_settings

    def run(self):
        self.log_msg("Loading ML model..")
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts\\cow_bot\\weights\\best.pt'))
        self.log_msg("Model loaded successfully..")

        file_worker.load_templates(file_worker.PATH_TO_ITEMS)
        file_worker.load_templates(file_worker.PATH_TO_DIGITS)

        start = time.time()
        utilities.setup_rs_client(self.mouse, zoomed_in=True)
        self.log_msg("Setting up client..")

        pyautogui.keyUp("up")
        time.sleep(random.uniform(0.92, 1.84))
        pyautogui.keyDown('up')

        while self.check_stop_state():
            if self.pause():
                time.sleep(1)
                continue

            if time.time() - start > self.script_info["run_time"] * 60:
                self.log_msg("Script run time finished. Stopping..")
                self.stop()
                break

            if not self.try_attack_nearest_enemy():
                continue

            current_time = time.time()
            while time.time() - current_time < 6:
                img = np.array(utilities.take_picture(save=False, screen=dictionary.health_bar))
                self.is_in_combat = object_detector.is_pixel_count_enough(img, [60, 100, 100], [60, 255, 255], 25)

                if self.is_in_combat:
                    break

            if not self.is_in_combat:
                self.log_msg("Player doesn't seem to be in combat.. Retrying..")
                continue

            self.log_msg("In combat with a cow..")

            while self.is_in_combat and self.check_stop_state():
                time.sleep(1)
                self.is_in_combat = object_detector.is_pixel_count_enough(np.array(utilities.take_picture(save=False, screen=dictionary.health_bar)), [60, 100, 100], [60, 255, 255], 25)
                health_count = int(object_detector.detect_orb_values('hp'))

                if health_count <= 10:
                    if self.eat_food():
                        if int(object_detector.detect_orb_values()) > health_count:
                            self.log_msg(f"Eat {self.script_info['item']}")
                    else:
                        break

            if self.check_stop_state():
                self.kill_count.set(self.kill_count.get() + 1)
                self.log_msg("Out of combat..")
            self.index = 0
        self.stop()

    def try_attack_nearest_enemy(self):
        img = np.array(utilities.take_picture(save=False, screen=dictionary.game_screen))
        prediction = self.model(img)
        npa = prediction.pandas().xyxy[0].to_numpy()

        if len(npa) == 0:
            self.log_msg("Didn't detect any cows around..")
            return False

        enemy = None

        for detection in npa:
            xmin, ymin, xmax, ymax = detection[:4]

            cropped_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]
            if object_detector.is_pixel_count_enough(cropped_img, [60, 100, 100], [60, 255, 255], 10):
                continue
            enemy = detection
            break

        if enemy is None:
            self.log_msg("All cows are in combat..")
            return False

        xmin, ymin, xmax, ymax = enemy[:4]
        # cv.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        x_center = int((xmax - xmin) / 2) + int(xmin)
        y_center = int((ymax - ymin) / 2) + int(ymin)

        utilities.move_mouse(self.mouse, x_center + dictionary.game_screen[0], y_center + dictionary.game_screen[1], click=False)
        img = np.array(utilities.take_picture(save=False, screen=dictionary.cow_text))

        if object_detector.is_pixel_count_enough(img, [25, 100, 100], [31, 255, 255], 70):
            pyautogui.click()
            self.log_msg('Attacking cow..')
            return True
        else:
            self.log_msg("No cow at that position.. Trying again..")
            return False

    def eat_food(self):
        food = self.script_info['item']
        foods = object_detector.match_templates(food, 0.90)

        if len(foods) == 0:
            self.log_msg("Preferred food hasn't been found..\nStopping the script..")
            self.running = False
            return False

        coords = random.choice(foods)
        target_x = int((coords[0][0] + coords[1][0]) / 2)
        target_y = int((coords[0][1] + coords[1][1]) / 2)
        utilities.move_mouse(self.mouse, target_x + dictionary.bag_screen[0], target_y + dictionary.bag_screen[1], click=True)

        return True

    def check_stop_state(self):
        return self.running and self.was_stopped()
