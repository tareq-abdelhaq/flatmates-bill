from flat import Bill, Flatmate
from reports import PDFReport

amount = float(input("Hey, enter the bill amount: "))
period = input("Enter the bill period? E.g. December 2020: ")

flatmate1_name = input("What's your name? ")
flatmate1_days_in_house = int(
    input(
        f"How many days did {flatmate1_name} stayed in the house during the bill period: "
    )
)

flatmate2_name = input("What's the name of the other flatmate? ")
flatmate2_days_in_house = int(
    input(
        f"How many days did {flatmate2_name} stayed in the house during the bill period: "
    )
)

bill = Bill(amount, period)

flatmate1 = Flatmate(name=flatmate1_name, days_in_house=flatmate1_days_in_house)
flatmate2 = Flatmate(name=flatmate2_name, days_in_house=flatmate2_days_in_house)

print(f"{flatmate1.name.capitalize()} pays: {flatmate1.pays(bill, flatmate2)!s}")
print(f"{flatmate2.name.capitalize()} pays: {flatmate2.pays(bill, flatmate1)!s}")

pdf_report = PDFReport(name=f"bill_{bill.period}.pdf")
pdf_report.generate(flatmate1, flatmate2, bill)
