from random import randint, uniform, triangular
from utils.bar import Bar

class Clients(Bar):
    def __init__(self, config) -> None:
        self.drinks = config['clients']['bar']['drinks']
        self.drinks_demand_min = config['clients']['bar']['drinks_demand_min']
        self.drinks_demand_max = config['clients']['bar']['drinks_demand_max']

        self.food = config['clients']['bar']['food']
        self.food_demand_min = config['clients']['bar']['food_demand_min']
        self.food_demand_max = config['clients']['bar']['food_demand_max']

        self.clients_amount = config['clients']['start_amount']
        self.entrance_fee = config['clients']['entrance_fee']

        self.today_client_amount = 0 

        self.last_iter_incident = 0
        self.incident_range_down = 7
        self.incident_range_up = 30
        self.incident_min = config['clients']['incident_min']
        self.incident_max = config['clients']['incident_max']

        super().__init__()

    def __calculate_today_client_amount(self):
        up_client_amount = int(self.clients_amount + (Bar.reputation_level // 100) * 20)
        self.today_client_amount = int(randint(self.clients_amount, up_client_amount) * self.get_multiplier())
        print('today_client_amount', self.today_client_amount)

    def __buy(self, item):
        today_profit = 0

        if item == 'drinks':
            min_demand, max_demand = self.drinks_demand_min, self.drinks_demand_max
            items = self.drinks
        else: 
            min_demand, max_demand = self.drinks_demand_min, self.drinks_demand_max
            items = self.drinks
       
        today_item_demand = int(round(uniform(min_demand, max_demand), 1) * self.today_client_amount)
        mean_item_amount = today_item_demand // len(item)

        for item in items:
            max_amount = min(mean_item_amount, item['max_amount'])
            today_profit += item['price'] * max_amount

        return today_profit

    def __pay_entrance(self):
        return self.today_client_amount * self.entrance_fee

    def launch_clients(self, iteration):
        if not super().check_working_day(): return

        self.__calculate_today_client_amount()

        entrance_income = self.__pay_entrance()
        drinks_income = self.__buy('drinks')
        food_income = self.__buy('food')
        overall_income = entrance_income + drinks_income + food_income

        expenses = self.__try_invoke_incident(iteration)

        self.push_income(overall_income)
        self.push_expenses(expenses)
        self.push_visitors(self.today_client_amount)

    def __try_invoke_incident(self, iteration):
        if iteration - self.last_iter_incident >= randint(self.incident_range_down, self.incident_range_up):
            self.last_iter_incident = iteration
            return 0 - int(triangular(self.incident_min, self.incident_max, 0.1))
        return 0