# Flatmates Bill

A web app, built with [Flask](https://flask.palletsprojects.com/) and [Flask-WTF](https://flask-wtf.readthedocs.io/), that splits a shared bill between two flatmates in proportion to the number of days each one stayed in the house during the bill period. The user fills in a form with the bill amount, the period and each flatmate's name and days stayed. The app calculates what each flatmate owes, generates a PDF report, uploads it to [Filestack](https://www.filestack.com/) and gives the user a link to download it.

## Pages

| Page | Route | Description |
|---|---|---|
| Home | `/` | Introduces the app and has a link to the bill form page |
| Bill form | `/bill` | A CSRF-protected form (Flask-WTF) with the bill amount, the bill period (e.g. `December 2020`), and each flatmate's name and days stayed, plus a **Calculate** submit button |
| Results | `/results` | Shows a link to download the generated PDF report |

Each flatmate's share is `days_in_house / (total days of both) * bill amount`.

### How a submission works

1. The form is validated: every field is required, the amount must be positive, days can't be negative, and the two flatmates can't both have 0 days.
2. The PDF is generated into `generated_reports/` under a unique name (`bill_<period>_<random>.pdf`), so simultaneous submissions never collide.
3. The PDF is uploaded to Filestack. The local copy is deleted afterwards, whether the upload succeeded or not.
4. On success, the Filestack URL is stored in the signed session and the user is redirected to the results page. On failure, the form is shown again with an error message and the entered values are kept.

While the report is being generated, the **Calculate** button is disabled and a progress message is shown ([`src/static/bill.js`](src/static/bill.js)), so the form can't be submitted twice.

The results page reads the URL from the session, so opening `/results` without having submitted a bill redirects to the form. The Filestack link is public: anyone who has it can download the report.

## Requirements

- Python 3.12 (see [`.python-version`](.python-version))
- Dependencies listed in [`requirements.txt`](requirements.txt) (includes Flask and Flask-WTF)
- A Filestack API key

## Setup

```bash
# 1. Make sure you are using Python 3.12
#    (pyenv and uv read .python-version automatically)
python3 --version

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. Configure your environment variables
cp .env.example .env
#    then edit .env and set FILESTACK_API_KEY and SECRET_KEY
```

### Configuration

Secrets are read from environment variables, loaded from a `.env` file in the project root by [`src/config.py`](src/config.py). `.env` is git-ignored; [`.env.example`](.env.example) is committed as a template.

| Variable | Description |
|---|---|
| `FILESTACK_API_KEY` | API key used to upload the PDF report to Filestack |
| `SECRET_KEY` | Secret used by Flask / Flask-WTF to sign sessions and CSRF tokens. Generate one with `python -c "import secrets; print(secrets.token_hex(32))"` |

To use a new variable in code:

```python
from config import require_env

value = require_env("MY_VARIABLE")  # raises RuntimeError if missing or empty
```

## Usage

Start the development server (it can be run from any directory):

```bash
python src/main.py
```

Then open <http://127.0.0.1:5000/> in your browser. The server runs with `debug=True`, which is meant for local development only; don't use it to serve the app publicly.

## Design

| Class | Module | Attributes / Methods |
|---|---|---|
| `Bill` | [`src/flat.py`](src/flat.py) | `amount`, `period`, `currency` (default `E£`) |
| `Flatmate` | [`src/flat.py`](src/flat.py) | `name`, `days_in_house`, `pays(bill, co_flatmate)` |
| `PDFReport` | [`src/reports.py`](src/reports.py) | `name`, `filepath` (property), `generate(flatmate1, flatmate2, bill)` |
| `FileSharer` | [`src/reports.py`](src/reports.py) | `filepath`, `share()` (uploads the file and returns its URL) |
| `BillForm` | [`src/main.py`](src/main.py) | Flask-WTF form with the validated bill and flatmate fields |
| `HomePage`, `BillPage`, `ResultsPage` | [`src/main.py`](src/main.py) | Flask `MethodView` classes for the three pages |

A form object is created inside each request handler, never as a class attribute: it reads the current request and CSRF token, so a shared instance would fail at import time and leak one user's data to another.

## Project structure

```
flatmates-bill/
├── assets/              # images used in the PDF report
├── generated_reports/   # generated PDF reports (contents are git-ignored)
├── src/
│   ├── main.py          # Flask app: routes, BillForm and entry point
│   ├── config.py        # loads .env and exposes require_env()
│   ├── flat.py          # Bill and Flatmate classes
│   ├── reports.py       # PDFReport and FileSharer classes
│   ├── templates/       # Jinja templates: index.html, bill.html, results.html
│   └── static/          # style.css and bill.js (disables the submit button while working)
├── .env.example         # template for required environment variables
├── requirements.txt     # pinned dependencies
├── .python-version      # Python version used for development
└── .gitignore
```
