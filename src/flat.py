class Flatmate:
    """
    Class that represents a flatmate and contains data about a flatmate, such as name, days stayed in house and others. they live in a shared flat and pay for bills.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(self, bill: "Bill", co_flatmate: "Flatmate"):
        weight = self.days_in_house / (self.days_in_house + co_flatmate.days_in_house)
        return weight * bill.amount


class Bill:
    """
    Class that represents a bill and contains data about a bill, such as amount, period and others.
    """

    def __init__(self, amount, period, currency="E£"):
        self.amount = amount
        self.currency = currency
        self.period = period
