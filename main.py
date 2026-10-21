from getpass import getpass

from auth import signup, login
from database import get_transactions
from transactions import prompt_add_transaction, prompt_update_transaction


def main():

    userId = None

    while True:
        print("\n=== Budget Tracker ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. View Transactions")
        print("4. Add Transaction")
        print("5. Update Transaction")
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            username = input("Username: ")
            password = getpass("Password: ")

            try:
                user_id = signup(username, password)
                print(f"Account created! Your user ID is {user_id}.")
            except Exception as e:
                print(f"Could not create account: {e}")

        elif choice == "2":
            username = input("Username: ")
            password = getpass("Password: ")

            user_id = login(username, password)

            if user_id is None:
                print("Invalid username or password.")
                continue

            print(f"\nLogged in as {username}")
            userId = user_id

        elif choice == "3":
            if userId is None:
                print("You must be logged in to view transactions.")
                continue

            transactions = get_transactions(userId)

            if not transactions:
                print("No transactions found.")
            else:
                print("\nTransactions:")
                print("Transaction ID | Amount | Category | Payment Method | Date | Description")
                for transaction in transactions:
                    print(transaction)

        elif choice == "4":
            if userId is None:
                print("You must be logged in to add transactions.")
                continue
            prompt_add_transaction(userId)

        elif choice == "5":
            if userId is None:
                print("You must be logged in to update transactions.")
                continue
            prompt_update_transaction(userId)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
