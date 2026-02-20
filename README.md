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
uv run python main.py <path_to_file.json> 
```

`uv run` executes commands inside the project environment and ensures it is up-to-date before running.

Examples (from the notebook):

```bash
uv run python main.py files/tests/test_valid.json
```

---

## Dev checks (linting & typing)

Run these from the repo root:

```bash
uv run flake8 main.py
uv run pylint main.py
```

(These are also demonstrated in `evidence.ipynb`.)
