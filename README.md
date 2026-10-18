# Flatmates Bill

A command-line app that splits a shared bill between two flatmates in proportion to the number of days each one stayed in the house during the bill period. It asks for the bill amount, the period and each flatmate's name and days stayed, prints what each one owes, then generates a PDF report and opens it in your default web browser.

## Requirements

- Python 3.12 (see [`.python-version`](.python-version))
- Dependencies listed in [`requirements.txt`](requirements.txt)

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
```

## Usage

Run the app from the project root, because the logo is loaded from the relative path `./assets/house.png`:

```bash
python src/main.py
```

You will be prompted for:

1. The bill amount
2. The bill period (e.g. `December 2020`)
3. The name of the first flatmate and the days they stayed in the house
4. The name of the other flatmate and the days they stayed in the house

Each flatmate's share is `days_in_house / (total days of both) * bill amount`. The report is saved to `generated_reports/bill_<period>.pdf` and opened in your default browser.

## Design

| Class | Module | Attributes / Methods |
|---|---|---|
| `Bill` | [`src/flat.py`](src/flat.py) | `amount`, `period`, `currency` (default `E£`) |
| `Flatmate` | [`src/flat.py`](src/flat.py) | `name`, `days_in_house`, `pays(bill, co_flatmate)` |
| `PDFReport` | [`src/reports.py`](src/reports.py) | `name`, `generate(flatmate1, flatmate2, bill)` |

## Project structure

```
flatmates-bill/
├── assets/              # images used in the PDF report
├── generated_reports/   # generated PDF reports (contents are git-ignored)
├── src/
│   ├── main.py          # entry point (prompts for input and runs the app)
│   ├── flat.py          # Bill and Flatmate classes
│   └── reports.py       # PDFReport class
├── requirements.txt     # pinned dependencies
├── .python-version      # Python version used for development
└── .gitignore
```
