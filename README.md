# Budget Tracker

A Python command-line budget tracker using SQLite Cloud and Argon2 password hashing.

## Requirements

- Python 3 and pip
- A SQLite Cloud database and API key
- Internet access to connect to SQLite Cloud

## Setup

Run these commands from the project directory.

### 1. Create and activate a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, use:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If pip is missing, run `python -m ensurepip --upgrade` first.

### 3. Configure the database

Create a local `env.py` file in the project root with your SQLite Cloud connection URL:

```python
DATABASE_URL = "sqlitecloud://YOUR_HOST:8860/budget_tracker.sqlite?apikey=YOUR_API_KEY"
```

Replace `YOUR_HOST`, `YOUR_API_KEY`, and the database name with the values for your SQLite Cloud database.

### 4. Run the app

```sh
python main.py
```
