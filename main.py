from getpass import getpass

from auth import signup, login
from database import get_transactions, track_spending
from tabulate import tabulate


def main():

    userId = None

    while True:
        print("\n=== Budget Tracker ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. View Transactions")
        print("4. Track Spending")
        print("5. Exit")

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
                headers = [ 
                    'transaction_date', 
                    'description',
                    'payment_method', 
                    'transaction_Id',
                    'amount'    
                ]
                print("\nTransactions:")
                print(tabulate(transactions, headers=headers, tablefmt='grid'))

        elif choice == '4':
            if userId is None:
                print("You must be logged in to view transactions.")
                continue
            
            tracking = track_spending(userId)
            if not tracking:
                print("Error. Please come back later.")
            else:
                headers = ['Total Income', 'Total Expenses', 'Account Balance']
                print("\nHere is a summary of your cash flow:")
                print(tabulate(tracking, headers=headers, tablefmt='grid'))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()