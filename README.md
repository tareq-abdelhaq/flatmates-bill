# Flatmates Bill

A command-line app that splits a shared bill between two flatmates in proportion to the number of days each one stayed in the house during the bill period. It asks for the bill amount, the period and each flatmate's name and days stayed, prints what each one owes, generates a PDF report, uploads it to [Filestack](https://www.filestack.com/) and prints a shareable URL. The local PDF is deleted after a successful upload.

## Requirements

- Python 3.12 (see [`.python-version`](.python-version))
- Dependencies listed in [`requirements.txt`](requirements.txt)
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

# 4. Configure your API key
cp .env.example .env
#    then edit .env and set FILESTACK_API_KEY
```

### Configuration

Secrets are read from environment variables, loaded from a `.env` file in the project root by [`src/config.py`](src/config.py). `.env` is git-ignored; [`.env.example`](.env.example) is committed as a template.

| Variable | Description |
|---|---|
| `FILESTACK_API_KEY` | API key used to upload the PDF report to Filestack |

To use a new variable in code:

```python
from config import require_env

value = require_env("MY_VARIABLE")  # raises RuntimeError if missing or empty
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

Each flatmate's share is `days_in_house / (total days of both) * bill amount`. The report is saved to `generated_reports/bill_<period>.pdf`, uploaded to Filestack, and the resulting URL is printed. After a successful upload the local PDF is removed; if the upload fails, the file is kept.

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
│   ├── main.py          # entry point (prompts for input and runs the app)
│   ├── config.py        # loads .env and exposes require_env()
│   ├── flat.py          # Bill and Flatmate classes
│   └── reports.py       # PDFReport and FileSharer classes
├── .env.example         # template for required environment variables
├── requirements.txt     # pinned dependencies
├── .python-version      # Python version used for development
└── .gitignore
```
