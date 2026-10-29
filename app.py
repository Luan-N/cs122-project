from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Flask, jsonify, redirect, render_template, request, session

from auth import login, signup
from database import (
    add_transaction,
    delete_transaction,
    get_transactions,
    search_transaction,
    update_transaction,
)
from env import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.get("/")
def home():
    return redirect("/login")


@app.get("/login")
def login_page():
    if session.get("user_id") is not None:
        return redirect("/dashboard")

    return render_template("login.html")


@app.get("/signup")
def signup_page():
    if session.get("user_id") is not None:
        return redirect("/dashboard")

    return render_template("signup.html")


@app.get("/dashboard")
def dashboard_page():
    if session.get("user_id") is None:
        return redirect("/login")

    return render_template("dashboard.html")


@app.post("/api/signup")
def signup_route():
    data = request.get_json()

    try:
        user_id = signup(data["username"], data["password"])
    except Exception:
        return {"error": "Username may already exist"}, 409

    return {"user_id": user_id}, 201


@app.post("/api/login")
def login_route():
    data = request.get_json()

    user_id = login(data["username"], data["password"])

    if user_id is None:
        return {"error": "Invalid username or password"}, 401

    session.clear()
    session["user_id"] = user_id

    return {"message": "Logged in"}


@app.post("/api/logout")
def logout_route():
    session.clear()
    return {"message": "Logged out"}


@app.get("/api/me")
def current_user_route():
    user_id = session.get("user_id")

    if user_id is None:
        return {"logged_in": False}, 401

    return {"logged_in": True, "user_id": user_id}


@app.get("/api/transactions")
def transactions_route():
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "Login required"}, 401

    transactions = get_transactions(user_id)

    return jsonify(transactions)


@app.post("/api/transactions")
def add_transaction_route():
    user_id = session.get("user_id")
    if user_id is None:
        return {"error": "Login required"}, 401

    data = request.get_json(silent=True) or {}
    try:
        amount = Decimal(str(data["amount"]))
        if not amount.is_finite() or amount == 0 or amount.as_tuple().exponent < -2:
            raise ValueError
        category = data["category"].strip()
        if not category:
            raise ValueError
        transaction_date = data.get("transaction_date") or date.today().isoformat()
        date.fromisoformat(transaction_date)
    except (AttributeError, KeyError, TypeError, InvalidOperation, ValueError):
        return {"error": "Valid amount, category, and date are required"}, 400

    try:
        transaction_id = add_transaction(
            user_id=user_id,
            amount=float(amount),
            category=category,
            payment_method=data.get("payment_method"),
            transaction_date=transaction_date,
            description=data.get("description"),
        )
    except Exception:
        return {"error": "Could not add transaction"}, 500

    return {"transaction_id": transaction_id}, 201


@app.put("/api/transactions/<int:transaction_id>")
def update_transaction_route(transaction_id):
    user_id = session.get("user_id")
    if user_id is None:
        return {"error": "Login required"}, 401

    data = request.get_json(silent=True) or {}
    try:
        amount = Decimal(str(data["amount"]))
        if not amount.is_finite() or amount == 0 or amount.as_tuple().exponent < -2:
            raise ValueError
        category = data["category"].strip()
        if not category:
            raise ValueError
        transaction_date = data["transaction_date"]
        date.fromisoformat(transaction_date)
    except (AttributeError, KeyError, TypeError, InvalidOperation, ValueError):
        return {"error": "Valid amount, category, and date are required"}, 400

    try:
        updated = update_transaction(
            user_id=user_id,
            transaction_id=transaction_id,
            amount=float(amount),
            category=category,
            payment_method=data.get("payment_method"),
            transaction_date=transaction_date,
            description=data.get("description"),
        )
    except Exception:
        return {"error": "Could not update transaction"}, 500

    if not updated:
        return {"error": "Transaction not found"}, 404

    return {"message": "Transaction updated"}


@app.delete("/api/transactions/<int:transaction_id>")
def delete_transaction_route(transaction_id):
    user_id = session.get("user_id")
    if user_id is None:
        return {"error": "Login required"}, 401

    try:
        deleted = delete_transaction(user_id, transaction_id)
    except Exception:
        return {"error": "Could not delete transaction"}, 500

    if not deleted:
        return {"error": "Transaction not found"}, 404

    return {"message": "Transaction deleted"}


@app.get("/api/dashboard")
def dashboard_data_route():
    user_id = session.get("user_id")
    if user_id is None:
        return {"error": "Login required"}, 401

    month = request.args.get("month") or date.today().strftime("%Y-%m")
    try:
        if len(month) != 7 or month[4] != "-":
            raise ValueError
        date.fromisoformat(f"{month}-01")
    except ValueError:
        return {"error": "Month must use YYYY-MM format"}, 400

    transactions = search_transaction(user_id, month)

    income = sum(float(row[5]) for row in transactions if float(row[5]) > 0)
    expenses = sum(abs(float(row[5])) for row in transactions if float(row[5]) < 0)
    return {
        "transactions": transactions,
        "month": month,
        "summary": {
            "income": income,
            "expenses": expenses,
            "balance": income - expenses,
            "expense_to_income_ratio": expenses / income if income else None,
        },
    }


@app.get("/api/transactions/search")
def search_transactions_route():
    user_id = session.get("user_id")
    if user_id is None:
        return {"error": "Login required"}, 401

    month = request.args.get("month", "")
    try:
        if len(month) != 7 or month[4] != "-":
            raise ValueError
        date.fromisoformat(f"{month}-01")
    except ValueError:
        return {"error": "Month must use YYYY-MM format"}, 400

    return jsonify(search_transaction(user_id, month))

if __name__ == '__main__':  
   app.run()  
