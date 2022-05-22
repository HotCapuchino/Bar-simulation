from time import sleep
import keyboard


iteration_len = 1

income = []
expenses = []
club_popularity = 0 # максимум 1000, раз в 30-60 итераций, максимальный плюс (25), максимальный минус (50)

while True:
    # здесь должны вызываться какие-то функции

    # на основе результатов заполняются ячейки в массивах доходов и расходов
    sleep(iteration_len)

    if keyboard.is_pressed('q'):
        break

# формируем графики с доходами и расходами и на основе их формируем график с прибылью
# график с популярностью