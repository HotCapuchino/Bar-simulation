import sys
from time import sleep
# Использование библиотеки на линукс требует рута -> sudo pip3 install keyboard, запускать скрипт от sudo
import keyboard
import json


def load_config(file_path):
    try:
        file = open(file_path)
        config = json.load(file)
        file.close()
        return config
    except Exception:
        print("Error while reading json file!")
        sys.exit(-1)

GENERAL_CONFIG_FILE_PATH = 'resources/config.json'
ARTISTS_CONFIG_FILE_PATH = 'resources/artists.json'
MACRO_CONFIG_FILE_PATH = 'resources/macro.json'

GENERAL_CONFIG = load_config(GENERAL_CONFIG_FILE_PATH)
ARTISTS_CONFIG = load_config(ARTISTS_CONFIG_FILE_PATH)
MACRO_CONFIG = load_config(MACRO_CONFIG_FILE_PATH)

ITERATION_LEN = GENERAL_CONFIG['iteration_len']

income = []
expenses = []
club_popularity = 0 # максимум 1000, раз в 30-60 итераций, максимальный плюс (25), максимальный минус (50)

while True:
    # здесь должны вызываться какие-то функции

    # на основе результатов заполняются ячейки в массивах доходов и расходов
    sleep(ITERATION_LEN)

    if keyboard.is_pressed('q'):
        break

# формируем графики с доходами и расходами и на основе их формируем график с прибылью
# график с популярностью