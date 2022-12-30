import os
import re
import cv2 as cv
from dictionary import templates, scripts, action_list

PATH_TO_ITEMS = os.path.join("data", "items")
PATH_TO_DIGITS = os.path.join("data", "digits")
FILE_PATH = os.path.dirname(os.path.realpath(__file__))
LOGS_DIC = os.path.join(FILE_PATH, 'script_logs')


def load_templates(path):
    files = os.listdir(os.path.join(FILE_PATH, path))

    for file in files:
        template = cv.imread(os.path.join(FILE_PATH, path, file), 0)
        w, h = template.shape
        templates[file[:file.index('.')]] = (template, w, h)


def load_scripts():
    with open(os.path.join('../scripts', 'bots.txt')) as file:
        for line in file:
            bot = re.findall("([^,]*),", line)
            scripts.append(bot[0])
            action_list[bot[0]] = [x.strip() for x in bot[1:]]


def save_logs(logs, name, date):
    file = open("{0}\\{1}-{2}.txt".format(LOGS_DIC, name, date), 'w')
    file.write(logs)
    file.close()
