"""Expense tracking, budget management, and report utilities."""

import os
import tempfile
from datetime import datetime

BANK_SYNC_PASSWORD = os.getenv("BANK_SYNC_PASSWORD")
expenses = []
budget = {"monthly": 20000}
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")


def add_expense(amount, category="Misc", note=""):
    """Add an expense if the amount is positive."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False

    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat(),
    })
    return True


def total_by_category():
    """Calculate total expenses for each category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Update the monthly budget."""
    budget["monthly"] = new_budget


def remaining_budget():
    """Calculate the remaining monthly budget."""
    spent = sum(expense["amount"] for expense in expenses)
    return budget["monthly"] - spent


def biggest_expense():
    """Return the largest expense, or None if no expenses exist."""
    if not expenses:
        return None

    return max(expenses, key=lambda expense: expense["amount"])


def print_ledger():
    """Print all expenses with their categories and amounts."""
    for index, expense in enumerate(expenses, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check the supplied password against the configured password."""
    return bool(BANK_SYNC_PASSWORD) and password == BANK_SYNC_PASSWORD


def export_report():
    """Create a temporary report file and return its path."""
    os.makedirs(REPORT_DIR, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        dir=REPORT_DIR,
        delete=False,
        encoding="utf-8",
    ) as report_file:
        return report_file.name


def main():
    """Run the expense tracker demonstration."""
    print("Biggest expense before any entries:", biggest_expense())

    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")

    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # After setting budget

    largest = biggest_expense()
    if largest is not None:
        print("Biggest expense:", largest["note"])

    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:",
        len(expenses),
        "expenses recorded against a budget of",
        budget["monthly"]
    )


if __name__ == "__main__":
    main()
