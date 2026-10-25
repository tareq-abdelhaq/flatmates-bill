from uuid import uuid4

from flask import Flask, flash, redirect, render_template, session, url_for
from flask.views import MethodView
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FloatField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange

from config import require_env
from flat import Bill, Flatmate
from reports import FileSharer, PDFReport

app = Flask(__name__)
app.config["SECRET_KEY"] = require_env("SECRET_KEY")


class HomePage(MethodView):
    def get(self):
        return render_template("index.html")


class BillForm(FlaskForm):
    amount = FloatField(
        "Bill Amount:", validators=[InputRequired(), NumberRange(min=0.01)]
    )
    period = StringField("Bill Period:", validators=[DataRequired()])

    name1 = StringField("Name:", validators=[DataRequired()])
    days_in_house1 = IntegerField(
        "Days in house:", validators=[InputRequired(), NumberRange(min=0)]
    )

    name2 = StringField("Name:", validators=[DataRequired()])
    days_in_house2 = IntegerField(
        "Days in house:", validators=[InputRequired(), NumberRange(min=0)]
    )

    submit = SubmitField("Calculate")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        # Flatmate.pays divides by the combined days, so they can't both be 0
        if (self.days_in_house1.data or 0) + (self.days_in_house2.data or 0) == 0:
            self.days_in_house2.errors = [
                "At least one flatmate must have stayed 1 or more days."
            ]
            return False
        return True


class BillPage(MethodView):
    def get(self):
        return render_template("bill.html", form=BillForm())

    def post(self):
        form = BillForm()
        if not form.validate_on_submit():
            return render_template("bill.html", form=form)

        bill = Bill(amount=form.amount.data, period=form.period.data)
        flatmate1 = Flatmate(name=form.name1.data, days_in_house=form.days_in_house1.data)
        flatmate2 = Flatmate(name=form.name2.data, days_in_house=form.days_in_house2.data)

        # The period is user input: sanitize it and add a random suffix so
        # simultaneous submissions never collide or escape the folder.
        filename = f"bill_{secure_filename(str(bill.period))}_{uuid4().hex[:8]}.pdf"
        pdf_report = PDFReport(name=filename)
        pdf_report.generate(flatmate1, flatmate2, bill)

        try:
            report_url = FileSharer(pdf_report.filepath).share()
        except Exception:
            app.logger.exception("Uploading the report failed")
            flash("Could not upload the report. Please try again.")
            return render_template("bill.html", form=form)
        finally:
            # Remove the local copy either way: on success it lives on Filestack,
            # and on failure a retry generates a fresh file with a new name.
            pdf_report.filepath.unlink(missing_ok=True)

        # The session is signed with SECRET_KEY, so the URL can't be tampered with
        session["report_url"] = report_url
        return redirect(url_for("results_page"))


class ResultsPage(MethodView):
    def get(self):
        report_url = session.get("report_url")
        if not report_url:
            return redirect(url_for("bill_page"))
        return render_template("results.html", report_url=report_url)


app.add_url_rule("/", view_func=HomePage.as_view("home_page"))
app.add_url_rule("/bill", view_func=BillPage.as_view("bill_page"))
app.add_url_rule("/results", view_func=ResultsPage.as_view("results_page"))

if __name__ == "__main__":
    app.run(debug=True)
