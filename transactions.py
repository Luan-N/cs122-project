from datetime import date
from decimal import Decimal, InvalidOperation

from database import add_transaction, get_transaction, update_transaction


def _prompt_transaction_fields(transaction=None):
    if transaction is not None:
        _, old_amount, old_category, old_payment, old_date, old_description = transaction
        print("Press Enter to keep each current value.")

    while True:
        try:
            prompt = "Amount (negative = expense, positive = income)"
            if transaction is not None:
                prompt += f" [{old_amount}]"
            value = input(f"{prompt}: ").strip()
            if not value and transaction is not None:
                amount = Decimal(str(old_amount))
                break
            amount = Decimal(value)
            if (not amount.is_finite() or amount == 0
                    or abs(amount) > Decimal("999999999999.99")
                    or amount != amount.quantize(Decimal("0.01"))):
                raise ValueError
            break
        except (InvalidOperation, ValueError):
            print("Enter a nonzero amount between -999999999999.99 and 999999999999.99 with at most 2 decimal places.")

    categories = [
        "Food", "Transport", "Housing", "Utilities", "Shopping",
        "Entertainment", "Health", "Salary", "Freelance", "Gift", "Investment", "Other"
    ]
    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            prompt = f"Category [{old_category}]" if transaction is not None else "Category"
            value = input(f"{prompt}: ").strip()
            if not value and transaction is not None:
                category = old_category
                break
            choice = int(value)
            if not 1 <= choice <= len(categories):
                raise ValueError
        except ValueError:
            print("Select a category number from the list.")
            continue

        category = categories[choice - 1]
        if category == "Other":
            category = input("Enter category name: ").strip()
            if not category:
                print("Category name cannot be empty.")
                continue
        break

    while True:
        prompt = (f"Date [{old_date}] (YYYY-MM-DD): " if transaction is not None
                  else "Date (YYYY-MM-DD, Enter for today): ")
        transaction_date = input(prompt).strip()
        if not transaction_date:
            transaction_date = old_date if transaction is not None else date.today().isoformat()
            break
        try:
            parsed_date = date.fromisoformat(transaction_date)
            if parsed_date.isoformat() != transaction_date:
                raise ValueError
            break
        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")

    if transaction is not None:
        payment_method = input(f"Payment method [{old_payment or ''}]: ").strip() or old_payment
        description = input(f"Description [{old_description or ''}]: ").strip() or old_description
    else:
        payment_method = input("Payment method (optional): ").strip() or None
        description = input("Description (optional): ").strip() or None

    return dict(amount=float(amount), category=category, payment_method=payment_method,
                transaction_date=transaction_date, description=description)


def prompt_add_transaction(user_id):
    fields = _prompt_transaction_fields()

    try:
        add_transaction(user_id, **fields)
    except Exception as e:
        print(f"Could not add transaction: {e}")
        return
    print("Transaction added.")


def prompt_update_transaction(user_id):
    while True:
        value = input("Transaction ID to update (Enter to cancel): ").strip()
        if not value:
            return
        try:
            transaction_id = int(value)
            if not 0 < transaction_id <= 9223372036854775807:
                raise ValueError
            break
        except ValueError:
            print("Enter a valid positive transaction ID.")

    try:
        transaction = get_transaction(user_id, transaction_id)
    except Exception as e:
        print(f"Could not load transaction: {e}")
        return
    if transaction is None:
        print("Transaction not found for your account.")
        return

    fields = _prompt_transaction_fields(transaction)
    try:
        updated = update_transaction(user_id, transaction_id, **fields)
    except Exception as e:
        print(f"Could not update transaction: {e}")
        return
    if updated:
        print("Transaction updated.")
    else:
        print("Transaction not found for your account.")
