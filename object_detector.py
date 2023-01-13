import cv2 as cv
import numpy as np
import file_worker
import dictionary
from dictionary import *
from utilities import take_picture


def get_screenshot_mask(img, lower, upper):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    lower = np.array(lower)
    upper = np.array(upper)

    return cv.inRange(hsv, lower, upper)


def is_pixel_count_enough(img, lower, upper, pixel_count):
    mask = get_screenshot_mask(img, lower, upper)
    non_zero = cv.findNonZero(mask)

    if non_zero is None or len(non_zero) == 0:
        return False

    return len(non_zero) > pixel_count


def get_pixel_location(img, lower, upper):
    center_x, center_y = int(img.width / 2), int(img.height / 2)
    closest = None

    mask = get_screenshot_mask(np.array(img), lower, upper)
    non_zero = cv.findNonZero(mask)

    if len(non_zero) == 0:
        return None

    for pos in non_zero:
        length = abs(pos[0][0] - center_x) + abs(pos[0][1] - center_y)
        if closest is None or length < closest[1]:
            closest = (pos[0], length)

    return closest[0].tolist()


def match_orb_digits(img):
    keys = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for key in keys:
        needle = templates[f'{key}']
        if needle[0].shape != img.shape:
            continue
        difference = cv.subtract(img, needle[0])
        if np.max(difference) == 0:
            return str(key)
    return None


def detect_orb_values(key="hp"):
    ss = take_picture(False, screen=hp_orb if key == 'hp' else prayer_orb)
    mask = get_screenshot_mask(np.array(ss), [0, 100, 100], [60, 255, 255])

    cnts, h = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    sorted_cnts = get_sorted_contours(cnts)
    values = []

    for cnt in sorted_cnts:
        cropped = mask[cnt[1]:cnt[1] + cnt[3], cnt[0]:+ cnt[0] + cnt[2]]
        value = match_orb_digits(cropped)
        if value is None:
            print("Failed to match digits")
            return None
        values.append(value)

    return ''.join(values)


def match_templates(name, threshold=0.95):
    # for template in templates:
    if name not in templates:
        return []
    template = templates[name]
    img = np.array(take_picture(False, False, bag_screen))
    img = cv.cvtColor(cv.cvtColor(img, cv.COLOR_RGB2BGR), cv.COLOR_BGR2GRAY)
    result = cv.matchTemplate(img, template[0], cv.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    locations = {}
    for pnt in zip(*loc[::-1]):
        cv.rectangle(img, pnt, (pnt[0] + template[2], pnt[1] + template[1]), (0,255, 0), 2)
        # cv.rectangle(game_client, pnt, (pnt[0] + template[1], pnt[1] + template[2]), (0,255,0), 1)
        if name in locations:
            locations[name].append((pnt, (pnt[0] + template[2], pnt[1] + template[1])))
        else:
            locations[name] = [(pnt, (pnt[0] + template[2], pnt[1] + template[1]))]

    return [] if locations.get(name, None) is None else locations[name]


def get_sorted_contours(cnts):
    rects = [cv.boundingRect(cnt) for cnt in cnts]
    boundingBoxes = sorted(rects, key=lambda b: b[0])

    return boundingBoxes


if __name__ == '__main__':
    ss = take_picture(False, screen=dictionary.health_bar)
    mask = get_screenshot_mask(np.array(ss), [60, 100, 100], [60, 255, 255])
    cv.imshow('mask', mask)
    cv.imshow('a', np.array(ss))
    cv.waitKey()