import webbrowser
from pathlib import Path

from fpdf import FPDF

from flat import Bill, Flatmate


class PDFReport:
    """
    Class responsible to generate PDF reports and it contains data about a PDF reports, such as name.
    """

    def __init__(self, name):
        self.name = name

    def generate(self, flatmate1: Flatmate, flatmate2: Flatmate, bill: Bill):
        pdf_path = Path(__file__).parent.parent / "generated_reports" / f"{self.name}"

        flatmate1_pay = (
            str(round(flatmate1.pays(bill, co_flatmate=flatmate2), 2))
            + " "
            + bill.currency
        )
        flatmate2_pay = (
            str(round(flatmate2.pays(bill, co_flatmate=flatmate1), 2))
            + " "
            + bill.currency
        )

        pdf = FPDF(orientation="portrait", unit="pt", format="A4")
        pdf.add_page()

        # Insert flatmate bill document icon as logo
        pdf.image(
            "./assets/house.png",
            w=30,
            h=30,
        )

        # Insert title
        pdf.set_font("times", style="B", size=24)
        pdf.cell(w=0, h=80, txt="Flatmates Bill", align="C", ln=1)  # type: ignore

        # Insert bill period label and value
        pdf.set_font("times", style="B", size=14)
        pdf.cell(w=60, h=20, txt="Period:")  # type: ignore
        pdf.cell(w=100, h=20, txt=bill.period, ln=1)  # type: ignore

        # Insert bill amount label and value
        pdf.cell(w=60, h=20, txt="Amount:")  # type: ignore
        pdf.cell(w=100, h=20, txt=f"{bill.amount!s} {bill.currency}", ln=1)  # type: ignore

        # Add vertical space between the bill details and the flatmates details
        pdf.cell(w=0, h=20, ln=1)

        # Insert flatmates and how much each one has to pay
        pdf.set_font("times", style="", size=12)
        pdf.cell(w=60, h=20, txt=f"{flatmate1.name}:")  # type: ignore
        pdf.cell(
            w=100,
            h=20,
            txt=flatmate1_pay,  # type: ignore
            ln=1,
        )

        pdf.cell(w=60, h=20, txt=f"{flatmate2.name}:")  # type: ignore
        pdf.cell(
            w=100,
            h=20,
            txt=flatmate2_pay,  # type: ignore
            ln=1,
        )

        # Save and open the PDF file via browser
        pdf.output(str(pdf_path))
        webbrowser.open(pdf_path.as_uri())
