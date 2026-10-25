from pathlib import Path

from filestack import Client
from fpdf import FPDF

from config import require_env
from flat import Bill, Flatmate


class PDFReport:
    """
    Class responsible to generate PDF reports and it contains data about a PDF reports, such as name.
    """

    def __init__(self, name):
        self.name = name

    @property
    def filepath(self) -> Path:
        return Path(__file__).parent.parent / "generated_reports" / self.name

    def generate(self, flatmate1: Flatmate, flatmate2: Flatmate, bill: Bill):
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
        logo_path = Path(__file__).parent.parent / "assets" / "house.png"
        pdf.image(
            str(logo_path),
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

        # Save the PDF
        pdf.output(str(self.filepath))


class FileSharer:
    """
    An Object that's responsible to share files through filestack-python and give back a URL to access the uploaded file.
    """

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def share(self):
        client = Client(require_env("FILESTACK_API_KEY"))

        if not self.filepath.exists() or not self.filepath.is_file():
            raise ValueError(f"Filepath is not valid: {self.filepath}")

        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
