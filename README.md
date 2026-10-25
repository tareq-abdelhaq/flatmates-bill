# Flatmates Bill

A web app, built with [Flask](https://flask.palletsprojects.com/) and [Flask-WTF](https://flask-wtf.readthedocs.io/), that splits a shared bill between two flatmates in proportion to the number of days each one stayed in the house during the bill period. The user fills in a form with the bill amount, the period and each flatmate's name and days stayed. The app calculates what each flatmate owes, generates a PDF report and gives the user a link to download it.

> **Status:** the web interface is being built. The calculation and PDF/upload logic (`src/flat.py`, `src/reports.py`) is done and reusable. The entry point [`src/main.py`](src/main.py) is still the original command-line version until the Flask app replaces it.

## Pages

| Page | Description |
|---|---|
| Home | Introduces the app and has a link to the bill form page |
| Bill form | A form (Flask-WTF, CSRF-protected) with the bill amount, the bill period (e.g. `December 2020`), and each flatmate's name and days stayed, plus a **Calculate** submit button |
| Results | Shows a link to download the generated PDF report |

Each flatmate's share is `days_in_house / (total days of both) * bill amount`. Reports are saved to `generated_reports/bill_<period>.pdf` and can be uploaded to [Filestack](https://www.filestack.com/) to get a shareable URL.

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

The web app's run command will be documented here once the Flask app is in place.

Until then, the original command-line version still works and can be run from any directory:

```bash
python src/main.py
```

It prompts for the bill amount, period, and each flatmate's name and days stayed, prints what each one owes, uploads the PDF to Filestack and prints the shareable URL. The local PDF is deleted after a successful upload; if the upload fails, the file is kept.

## Design

| Class | Module | Attributes / Methods |
|---|---|---|
| `Bill` | [`src/flat.py`](src/flat.py) | `amount`, `period`, `currency` (default `E£`) |
| `Flatmate` | [`src/flat.py`](src/flat.py) | `name`, `days_in_house`, `pays(bill, co_flatmate)` |
| `PDFReport` | [`src/reports.py`](src/reports.py) | `name`, `filepath` (property), `generate(flatmate1, flatmate2, bill)` |
| `FileSharer` | [`src/reports.py`](src/reports.py) | `filepath`, `share()` (uploads the file and returns its URL) |

## Project structure

```
flatmates-bill/
├── assets/              # images used in the PDF report
├── generated_reports/   # generated PDF reports (contents are git-ignored)
├── src/
│   ├── main.py          # entry point (currently the CLI; to be replaced by the Flask app)
│   ├── config.py        # loads .env and exposes require_env()
│   ├── flat.py          # Bill and Flatmate classes
│   └── reports.py       # PDFReport and FileSharer classes
├── .env.example         # template for required environment variables
├── requirements.txt     # pinned dependencies
├── .python-version      # Python version used for development
└── .gitignore
```
