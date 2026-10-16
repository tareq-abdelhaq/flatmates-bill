# Flatmates Bill

An app that takes the amount of a bill for a period and the number of days each flatmate stayed in the house during that period. It calculates how much each flatmate has to pay and generates a PDF report with the flatmates' names, the period, and the amount each one owes.

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

```bash
python main.py
```

## Design

| Class | Attributes / Methods |
|---|---|
| `Bill` | `amount`, `period` |
| `Flatmate` | `name`, `days_in_house`, `pays(bill)` |
| `PdfReport` | `filename`, `generate(flatmate1, flatmate2, bill)` |

## Project structure

```
flatmates-bill/
├── assets/            # images used in the PDF report
├── generated_reports/ # generated PDF reports (contents are git-ignored)
├── main.py            # entry point
├── requirements.txt   # pinned dependencies
├── .python-version    # Python version used for development
└── .gitignore
```
