class Bill:
    """
    Class that represents a bill and contains data about a bill, such as amount, period and others.
    """

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period


class Flatmate:
    """
    Class that represents a flatmate and contains data about a flatmate, such as name, days stayed in house and others. they live in a shared flat and pay for bills.
    """

    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house

    def pays(
        self,
        bill: Bill,
    ):
        pass


class PDFReport:
    """
    Class responsible to generate PDF reports and it contains data about a PDF reports, such as name.
    """

    def __init__(self, name):
        self.name = name

    def generate(self, flatmate1, flatmate2, bill):
        pass
