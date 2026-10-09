import sqlite3
import matplotlib.pyplot as plt

while True:
    print("\n------<<<  Welcome to CashFlow  >>>-----")
    print("1. Update transactions.") # update transactions
    print("2. Plot data from database.") # print table showing income and expense in months.
    print("3. Quit program\n") # exit program.

    choice = input("Choose an option (1-3): ")

    if choice == "1":
        # TODO: write a function that allow user to
        # update transactions.
        print('Your transaction is updated successfully.')

    elif choice == "2":
        # Get income data from database
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT Amount FROM cashflow WHERE Type = ?",
            ("income",)
        )

        rows = cursor.fetchall()
        conn.close()

        amounts = [
            row[0] for row in rows
            if row[0] is not None
        ]

        if not amounts:
            print("No income data found.")
            continue

        x = list(range(1, len(amounts) + 1))
        y = amounts
        title = "Income Data"

    elif choice == "3":
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Please try again.")
        continue

    # Create and display the plot
    plt.figure()
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel("Entry")
    plt.ylabel("Amount")
    plt.show()

print("Program finished.")