from getpass import getpass

from auth import signup, login
from database import get_transactions, track_spending, print_cash_flow
from tabulate import tabulate


def main():

    userId = None

    while True:
        print("\n===  Budget Tracker  ===")
        print("   1. Sign Up")
        print("   2. Login")
        print("   3. View Transactions")
        print("   4. Track Spending")
        print("   5. Update Transaction")
        print("   6. Exit")

        choice = input("Select an option: ")

        match choice:

            case "1":
                print("\nEnter your username and password to create a new account.")
                username = input("Username: ")
                password = getpass("Password: ")

                confirm = input("Confirm to signup (Y/N): ").upper()

                if confirm == 'Y': 
                    try:
                        user_id = signup(username, password)
                        print(f"\n*** Account created! Your user ID is {user_id}.***")
                    except Exception as e:
                        print(f"ERROR! Could not create account: {e}")
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
                    print("\nYou must be logged in to view transactions.")
                    continue

                transactions = get_transactions(userId)

                if not transactions:
                    print("No transactions found.")
                else:
                    headers = [ 
                        'Date', 
                        'Description',
                        'Payment_method', 
                        'Transaction_Id',
                        'Amount'    
                    ]
                    print("\nTransactions:")
                    print(tabulate(transactions, headers=headers, tablefmt='fancy_grid'))

            case "4":
                if userId is None:
                    print("\nYou must be logged in to view transactions.")
                    continue
                    
                tracking = track_spending(userId)
                if not tracking:
                    print("Error. Please come back later.")
                else:
                    headers = ['Total Income', 'Total Expenses', 'Account Balance']
                    print("\nHere is a summary of your cash flow:")
                    print(tabulate(tracking, headers=headers, tablefmt='fancy_grid'))
                    income, expenses, balance = tracking[0]
                    print_cash_flow(income, expenses)

            case "5":
                if userId is None:
                    print("\nYou must be logged in to manage transactions.")
                    continue
                
                print("\nPlease choose an option of what you want to do:")
                print("  [U] Update a transaction")
                print("  [D] Delete a transaction")
                print("  [I] Insert a transaction")
                edit_type = input("Select an action (U/D/I): ").upper()

                match edit_type:
                    case "U":
                        print("\n---- Update Transaction ---")
                        # TODO

                    case "D":
                        print("\n--- Delete Transaction ---")
                        # TODO
                        
                    case "I":
                        print("\n--- Insert Transaction ---")
                        # TODO
                        
                    case _:
                        print("\nInvalid option. Returning to main menu")

            case "6":
                print("\nGoodbye!")
                break

            case _:
             print("Invalid option.")


if __name__ == "__main__":
    main()