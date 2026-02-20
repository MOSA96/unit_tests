# Project Name

Brief description of what this project does.

## Requirements

- Python 3.10+
- `uv` — the fast Python package and environment manager

## Installation

### 1) Install `uv`

**macOS / Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
````

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Check installation:

```bash
uv --version
```

### 2) Set up the project

If you already have a `pyproject.toml`:

```bash
uv sync
```

## Usage

Run script:

```bash
uv run python main.py input.json
```

## Testing & Quality

Run tests:

```bash
uv run python -m unittest tests/test_hotel_management.py -v
```

Run pylint:

```bash
uv run pylint <path_to_file.py>
```

Run flake8:

```bash
uv run flake8 <path_to_file.py>
```