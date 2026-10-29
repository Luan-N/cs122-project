# Budget Tracker

A Flask web budget tracker with a command-line interface, SQLite Cloud storage, and Argon2 password hashing.

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

### 3. Configure local secrets

Create a local `env.py` file in the project root. Do not commit this file.

```python
DATABASE_URL = "sqlitecloud://YOUR_HOST:8860/budget_tracker.sqlite?apikey=YOUR_API_KEY"
SECRET_KEY = "your-long-random-flask-secret"
```

Replace `YOUR_HOST`, `YOUR_API_KEY`, and the database name with the values for your SQLite Cloud database.
Generate a Flask secret key with:

```sh
python3 -c "import secrets; print(secrets.token_hex(32))"
```

`SECRET_KEY` signs Flask session cookies so the server can verify logged-in sessions. Keep it private and do not change it while using the app.

### 4. Run the web app

```sh
flask --app app run --debug
```

Open `http://127.0.0.1:5000/login` in a browser.

The web app supports:

- Signup, login, logout, and signed sessions
- Month and year transaction filtering
- Income, expenses, balance, and expense ratio summaries
- Cumulative income and expense chart
- Add, edit, and delete transactions

### 5. Run the CLI app

```sh
python main.py
```

The CLI and web app use the same authentication and database modules.
