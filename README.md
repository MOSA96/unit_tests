# Unit Tests


The main script is `main.py`

---

## Repo structure

```
.
├── .gitignore                          # Git ignore rules
├── .python-version                     # Python version hint for local tooling
├── README.md                           # Project documentation
├── evidence.ipynb                      # Jupyter notebook with usage evidence
├── files
│   ├── results                         # Output files to compare output from main.py
│   │   ├── test_edge_cases_results.txt
│   │   ├── test_invalid_results.txt
│   │   ├── test_mixed_results.txt
│   │   └── test_valid_results.txt
│   └── tests                           # JSON input files for testing scenarios
│       ├── test_edge_cases.json
│       ├── test_invalid.json
│       ├── test_mixed.json
│       └── test_valid.json
├── main.py                             # Entry point: reads JSON inputs, writes results
├── pyproject.toml                      # Project metadata + dev tools config
├── src
│   ├── __init__.py
│   └── hotel_management.py             # Core hotel logic
├── tests
│   ├── __init__.py
│   └── test_hotel_management.py        # Unit tests
└── uv.lock                             # Locked dependency graph for reproducible installs
```

Notes:
- `pyproject.toml` sets `requires-python = ">=3.12"` and defines dev tools in a dependency group (flake8, mypy, pylint, ipykernel).
- The notebook shows example commands using the test files under `test_files/TC1`, `test_files/TC2`, and `test_files/TC3`.

---

## Prerequisites

- Python **3.12+**
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

---

## Install (recommended: uv sync)

From the repo root:

```bash
uv sync
```

This creates/updates the project virtual environment at `.venv` and installs dependencies from `uv.lock`. By default, `uv sync` performs an “exact” sync (it removes packages not in the lockfile).

---

## Run the script

General usage:

```bash
uv run python compute_sales.py <price_file.json> <sales_file.json>
```

`uv run` executes commands inside the project environment and ensures it is up-to-date before running.

Examples (from the notebook):

```bash
uv run python compute_sales.py test_files/TC1/TC1.ProductList.json test_files/TC1/TC1.Sales.json
uv run python compute_sales.py test_files/TC1/TC1.ProductList.json test_files/TC2/TC2.Sales.json
uv run python compute_sales.py test_files/TC1/TC1.ProductList.json test_files/TC3/TC3.Sales.json
```

Expected totals (from the notebook):

- TC1 → **2481.86**
- TC2 → **166,568.23**
- TC3 → **165,235.37** (includes errors for products missing in the price file)

---

## Dev checks (linting & typing)

Run these from the repo root:

```bash
uv run flake8 compute_sales.py
uv run mypy compute_sales.py
uv run pylint compute_sales.py
```

(These are also demonstrated in `result_notebook.ipynb`.)


## Continuous Integration (Linting & Typing)

This repository includes a GitHub Actions workflow that automatically runs static analysis checks on every `push`.

**Workflow file:**
- `.github/workflows/linters_ci.yml`

**What it does:**
- Checks out the repo
- Installs `uv` and Python (via `uv python install`)
- Installs dependencies using `uv sync`
- Runs:
  - `mypy` (type checking)
  - `pylint` (code quality)
  - `flake8` (linting / style)

The workflow fails if any of these checks fail.
