from getpass import getpass
from tabulate import tabulate
from auth import signup, login
from database import *
from transactions import *
from datetime import datetime

def main():
    userId = None

    while True:
        print("\n=== Budget Tracker ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. View Transactions")
        print("4. Add Transaction")
        print("5. Update Transaction")
        print("6. Delete Transaction")
        print("7. Track Spending")
        print("8. Search Transactions")
        print("9. Exit")

        choice = input("Select an option: ")

        match choice:
            case "1":
                print("\nEnter your username and password to create a new account.")
                username = input("Username: ")
                password = getpass("Password: ")
                confirm = input("Confirm to signup (Y/N): ").upper()

                if confirm == "Y":
                    try:
                        user_id = signup(username, password)
                        print(f"\nAccount created! Your user ID is {user_id}.")
                    except Exception as e:
                        print(f"Could not create account: {e}")
                else:
                    print("Sign up cancelled.")

            case "2":
                print("\nEnter your username and password to login.")
                username = input("Username: ")
                password = getpass("Password: ")
                user_id = login(username, password)

                if user_id is None:
                    print("Invalid username or password.")
                    continue

                print(f"\nLogged in as {username}")
                userId = user_id

            case "3":
                if userId is None:
                    print("You must be logged in to view transactions.")
                    continue

                transactions = get_transactions(userId)

                current = datetime.now().strftime("%B %Y")

                if not transactions:
                    print("No transactions found.")
                else:
                    headers = ["Transaction_ID", "Date", "Category", "Payment Method", "Description", "Amount"]
                    print(f"\nTransactions for {current}:")
                    print(tabulate(transactions, headers=headers, tablefmt="fancy_grid"))

            case "4":
                if userId is None:
                    print("You must be logged in to add transactions.")
                    continue
                prompt_add_transaction(userId)

            case "5":
                if userId is None:
                    print("You must be logged in to update transactions.")
                    continue
                prompt_update_transaction(userId)

            case "6":
                if userId is None:
                    print("You must be logged in to delete transactions.")
                    continue
                prompt_delete_transaction(userId)

            case "7":
                if userId is None:
                    print("You must be logged in to track spending.")
                    continue

                tracking = track_spending(userId)
                if not tracking:
                    print("Error. Please come back later.")
                else:
                    headers = ["Total Income", "Total Expenses", "Account Balance"]
                    print("\nHere is a summary of your cash flow:")
                    print(tabulate(tracking, headers=headers, tablefmt="fancy_grid"))
                    income, expenses, balance = tracking[0]
                    print_cash_flow(income, expenses)

            case "8":
                if userId is None:
                    print("You must be logged in to track spending.")
                    continue
                prompt_search_transaction(user_id)              

            case "9":
                print("Goodbye!")
                break

            case _:
                print("Invalid option.")


if __name__ == "__main__":
    main()