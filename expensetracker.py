import csv
import argparse
import os
from datetime import datetime, timedelta

CSV_FILE = "expenses.csv"


def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])


def add_expense(category, amount, note):
    date_str = datetime.now().strftime("%Y-%m-%d")
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, category, amount, note])
    print(f"Added: {amount} in {category} for '{note}' on {date_str}")


def list_expenses(period):
    now = datetime.now()
    if period == 'today':
        start_date = now.strftime("%Y-%m-%d")
    elif period == 'week':
        start_date = (now - timedelta(days=7)).strftime("%Y-%m-%d")
    elif period == 'month':
        start_date = (now - timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        print("Invalid period. Choose from 'today', 'week', 'month'.")
        return

    print(f"\nExpenses for: {period.capitalize()}\n{'-'*40}")
    total = 0
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Date'] >= start_date:
                print(f"{row['Date']} | {row['Category']} | {row['Amount']} | {row['Note']}")
                total += float(row['Amount'])
    print(f"\nTotal: {total:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Simple CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest='command')

    # Add command
    add_parser = subparsers.add_parser('add')
    add_parser.add_argument('--category', required=True)
    add_parser.add_argument('--amount', required=True, type=float)
    add_parser.add_argument('--note', default="")

    # List command
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--period', choices=['today', 'week', 'month'], default='today')

    args = parser.parse_args()

    init_csv()

    if args.command == 'add':
        add_expense(args.category, args.amount, args.note)
    elif args.command == 'list':
        list_expenses(args.period)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()