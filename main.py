import random
import sys
from time import sleep
# Использование библиотеки на линукс требует рута -> sudo pip3 install keyboard, запускать скрипт от sudo
import keyboard
import json
from utils import Staff
from utils import Clients
from utils import Bar
# from utils import Resources
# from utils import Equipment
# from utils import Room
from matplotlib import pyplot as plt


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
days_counter = 0 # начало с понедельника

bar = Bar()
staff = Staff(GENERAL_CONFIG)
clients = Clients(GENERAL_CONFIG)


def expenses(ITERATION_LEN, working_day):
    total = 0
    if ITERATION_LEN % 60 == 0 and working_day:  # rent
        total -= GENERAL_CONFIG["room"]["rent"]

    if ITERATION_LEN % 180 == 0 and working_day:  # repairing
        total -= random.triangular(GENERAL_CONFIG["room"]["repairing_min"], GENERAL_CONFIG["room"]["repairing_max"],
                                    0.1)

    if ITERATION_LEN % 60 == 0 and working_day:  # incident
        if random.randint(0, 1):
            total -= random.triangular(GENERAL_CONFIG["room"]["incident_min"],
                                        GENERAL_CONFIG["room"]["incident_max"], 0.1)

    if ITERATION_LEN % 30 == 0 and working_day:
        total -= GENERAL_CONFIG["resources"]["logistics"]

    if ITERATION_LEN % 14 == 0 and working_day:  # advertising
        total -= 60000  # зачем столько пунктов в рекламе?

    if ITERATION_LEN % 1 == 0 and working_day:  # drinks and food
        for i in GENERAL_CONFIG["resources"]["drinks_src"]:
            total -= i["amount"] * i["price"]
        for j in GENERAL_CONFIG["resources"]["food_src"]:
            total -= j["amount"] * j["price"]

    if ITERATION_LEN == 1 and working_day:  # equipment
        for i in GENERAL_CONFIG["equipment"]["list"]:
            total -= i["amount"] * i["price"]

    if ITERATION_LEN % 180 == 0 and working_day:
        for k in GENERAL_CONFIG["equipment"]["list"]:
            total -= (k["amount"] * k["price"]) * GENERAL_CONFIG["equipment"]["depreciation"]

    return total

while True:
    days_counter += 1

    # здесь должны вызываться какие-то функции
    staff.launch_staff(days_counter)
    clients.launch_clients(days_counter)
    exp = expenses(days_counter, bar.check_working_day())

    # на основе результатов заполняются ячейки в массивах доходов и расходов
    sleep(ITERATION_LEN)
    bar.push_expenses(exp)
    # print(f'Итерация № {days_counter}')
    # print(f'День {bar.current_day}')

    bar.next_day()

    if days_counter == 360:
        # print('income', bar.income)
        # print('expense', bar.expenses)
        bar.calculate_revenue()
        break

    if days_counter % 60 == 0 and Bar.reputation_level <= 1000:
        Bar.reputation_level += random.randint(60, 120)


    # if keyboard.is_pressed('q'):

exp = list(map(lambda x: x * -1, bar.expenses))
avg_rev = []
avg_exp = []
w = 30
for i in range(len(exp) - w):
    avg_exp.append(sum(exp[i:i+w]) / w)

for i in range(len(bar.revenue) - w):
    avg_rev.append(sum(bar.revenue[i:i+w]) / w)


plt.subplot(121)
plt.plot(list(filter(lambda x: x > 0, bar.income)))
plt.subplot(122)
plt.plot(list(filter(lambda x: x > 0, bar.visitors)))
plt.show()

plt.subplot(121)
plt.plot(list(map(lambda x: x * -1, bar.expenses)))
plt.subplot(122)
plt.plot(bar.revenue)
plt.show()


# print('rep', Bar.reputation_level)
# plt.subplot(141)
# plt.plot(list(filter(lambda x: x > 0, bar.income)))
# plt.subplot(142)
# plt.plot(avg_exp)
# plt.subplot(143)
# plt.plot(list(filter(lambda x: x > 0, bar.visitors)))
# plt.subplot(144)
# plt.plot(bar.revenue)
# plt.show()

print('Total revenue', round(bar.calculate_total_revenue()))

# формируем графики с доходами и расходами и на основе их формируем график с прибылью
# график с популярностью