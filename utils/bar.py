from enum import Enum

class Days(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY= 7

class Bar:
    current_day = Days.MONDAY
    weekend_days = [Days.MONDAY, Days.THURSDAY, Days.WEDNESDAY]
    reputation_level = 0
    income = [0]
    expenses = [0]
    revenue = [0]
    current_index = 0
    visitors = [0]

    def next_day(self):
        Bar.current_day = Days(1 if (Bar.current_day.value + 1) % (len(Days) + 1) == 0 else (Bar.current_day.value + 1) % (len(Days) + 1))
        Bar.current_index += 1
        if len(Bar.income) <= Bar.current_index:
            Bar.income.append(0)
        if len(Bar.expenses) <= Bar.current_index:
            Bar.expenses.append(0)
        if len(Bar.visitors) <= Bar.current_index:
            Bar.visitors.append(0)

    def check_working_day(self):
        return Bar.current_day not in Bar.weekend_days

    def get_multiplier(self):
        multiplier = Bar.reputation_level / 500
        return multiplier if multiplier > 1 else 1

    def push_income(self, income):
        Bar.income[Bar.current_index] += income

    def push_expenses(self, expenses):
        Bar.expenses[Bar.current_index] += expenses

    def push_visitors(self, visitors):
        Bar.visitors[Bar.current_index] = visitors

    def calculate_revenue(self):
        for income, expense in zip(Bar.income, Bar.expenses):
            Bar.revenue.append(income + expense) 
    
    def calculate_total_revenue(self):
        return sum(Bar.revenue)