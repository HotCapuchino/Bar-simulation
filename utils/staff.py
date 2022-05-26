from random import randint, triangular

from utils.bar import Bar


class Staff(Bar):

    def __init__(self, config):
        self.tax = 0
        self.team = config['staff']['team']
        self.tax_rate = config['staff']['tax_rate']
        self.incident_min = config['staff']['incident_min']
        self.incident_max = config['staff']['incident_max']

        self.last_iter_incident = 0
        self.incident_range_down = 14
        self.incident_range_up = 28

        self.last_iter_taxes = 0
        self.taxes_range = 365

        self.last_iter_salary = 0
        self.salary_range = 30

        super().__init__()

    def __count_overall_salary(self, iteration):
        if iteration - self.last_iter_salary >= self.salary_range:
            self.last_iter_salary = iteration
            overall = 0
            for member in self.team:
                overall += member['amount'] * member['salary']
            self.tax += overall * self.tax_rate
            return 0 - overall
        return 0

    def __get_tax(self, iteration):
        if iteration - self.last_iter_taxes >= self.taxes_range:
            self.last_iter_taxes = iteration
            buf = self.tax
            self.tax = 0
            return 0 - buf
        return 0

    def __try_invoke_incident(self, iteration):
        if iteration - self.last_iter_incident >= randint(self.incident_range_down, self.incident_range_up):
            self.last_iter_incident = iteration
            return 0 - int(triangular(self.incident_min, self.incident_max, 0.1))
        return 0
    
    def launch_staff(self, iteration):
        salary_expenses = self.__count_overall_salary(iteration)
        tax_expenses = self.__get_tax(iteration)
        incident_expenses = self.__try_invoke_incident(iteration)
        
        overall_expenses = salary_expenses + tax_expenses + incident_expenses
        self.push_expenses(overall_expenses)