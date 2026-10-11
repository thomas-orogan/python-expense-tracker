
import json
import os

FILE_NAME = "transactions.json"


def load_transactions():
    """Load saved transactions from the JSON file."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Could not read saved transactions.")
            return []

    return []


def save_transactions():
    """Save all transactions to the JSON file."""
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(transactions, file, indent=4)
    except OSError:
        print("Error: Could not save transactions.")
        return False

    return True


def calculate_totals():
    """Calculate total income, expenses, and balance."""
    total_income = 0
    total_expenses = 0

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]
        elif transaction["type"] == "expense":
            total_expenses += transaction["amount"]

    balance = total_income - total_expenses

    return total_income, total_expenses, balance


def add_transaction():
    """Add a new income or expense."""
    transaction_type = input(
        "Enter type (income/expense): "
    ).strip().lower()

    if transaction_type not in ["income", "expense"]:
        print("Invalid transaction type. Enter income or expense.")
        return

    try:
        amount = float(input("Enter amount: "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        return

    transaction = {
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description
    }

    transactions.append(transaction)

    if save_transactions():
        print("Transaction added and saved successfully!")
    else:
        transactions.pop()
        print("Transaction was not saved. Please try again.")


def view_transactions():
    """Display all transactions with their numbers."""
    print("\n--- TRANSACTIONS ---")

    if not transactions:
        print("No transactions found.")
        return

    for number, transaction in enumerate(transactions, start=1):
        print(f"\nTransaction {number}")
        print("Type:", transaction["type"].capitalize())
        print("Amount: ₦{:,.2f}".format(transaction["amount"]))
        print("Category:", transaction["category"])
        print("Description:", transaction["description"])
        print("--------------------")


def delete_transaction():
    """Delete a transaction and save the updated list."""
    if not transactions:
        print("No transactions to delete.")
        return

    view_transactions()

    try:
        number = int(
            input("Enter the transaction number to delete: ")
        )

        if number < 1 or number > len(transactions):
            print("Invalid transaction number.")
            return

        removed_transaction = transactions.pop(number - 1)

        if save_transactions():
            print("Transaction deleted successfully!")
        else:
            transactions.insert(number - 1, removed_transaction)
            print("Could not save the change. Transaction restored.")

    except ValueError:
        print("Please enter a valid whole number.")


def view_balance():
    """Display the financial summary."""
    income, expenses, balance = calculate_totals()

    print("\n--- FINANCIAL SUMMARY ---")
    print("Total income: ₦{:,.2f}".format(income))
    print("Total expenses: ₦{:,.2f}".format(expenses))
    print("Remaining balance: ₦{:,.2f}".format(balance))


def main():
    """Run the expense tracker menu."""
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add transaction")
        print("2. View balance")
        print("3. View transactions")
        print("4. Delete transaction")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_transaction()

        elif choice == "2":
            view_balance()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            delete_transaction()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Try again.")


transactions = load_transactions()


if __name__ == "__main__":
    main()


