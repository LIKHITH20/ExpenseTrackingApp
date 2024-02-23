import os.path
from expense import Expense
import calendar
import datetime

def main():
    print("🎯 Running Expense Tracker!")
    expense_file = "expenses.csv"
    
    while True:
    # Check if the expense file exists and is not empty
        if os.path.exists(expense_file) and os.path.getsize(expense_file) > 0:
            # Read the budget from the expense file
            budget = read_budget_from_file(expense_file)
        else:
            # Ask user for the initial budget if the file is empty
            budget = get_initial_budget()
            save_budget_to_file(budget, expense_file)

        # Get user expense or income input
        expense, is_income = get_user_expense_or_income(budget)

        if is_income:
            save_savings_to_file(expense, expense_file)

        if not is_income:
            # Save the user expenses to a file
            save_expense_to_file(expense, expense_file)
    
        # Summarize user expenses by reading the file
        summarize_expenses(expense_file, budget)

        if prompt_continue():
           #Continue adding expenses or income
            continue
        else:
            exit()


def get_initial_budget():
    while True:
        try:
            initial_budget = float(input("Enter your initial budget: "))
            if initial_budget >= 0:
                return initial_budget
            else:
                print("Invalid budget. Please enter a non-negative amount.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def read_budget_from_file(file_path):
    with open(file_path, "r") as file:
        first_line = file.readline().strip()
        budget = float(first_line.split(",")[1])
    return budget


def save_budget_to_file(budget, file_path):
    # Check if the file is empty
    is_empty = os.path.getsize(file_path) == 0
    
    # Update the budget value in the first line
    budget_line = f"Budget,{budget}\n"
    
    if is_empty:
        # Write the budget to the first line if the file is empty
        with open(file_path, "w") as file:
            file.write(budget_line)
    else:
        # Read existing content from the file
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Update the budget value in the first line
        lines[0] = budget_line
        
        # Write the updated content back to the file
        with open(file_path, "w") as file:
            file.writelines(lines)


def get_user_expense_or_income(budget):
    while True:
        user_input = input("Are you adding an expense or income? (expense/income): ").lower()
        if user_input == "expense":
            return get_user_expense(budget), False
        elif user_input == "income":
            return get_user_income(), True
        else:
            print("Invalid input. Please enter 'expense' or 'income'.")


def get_user_income():
    while True:
        try:
            income_amount = float(input("Enter income amount: "))
            if income_amount >= 0:
                
                return income_amount
            else:
                print("Invalid amount. Please enter a non-negative number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_user_expense(budget):
    print(f"🎯 Getting User Expense")
    expense_input = input("Enter expense name: ")
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount > budget:
                print("You're exceeding your budget limit. Please re-check the amount again")
            else:
                break
        except Exception:
            print("Enter a valid input, please try again!")
    expense_categories = ["Food", "Home", "Work","Fun","Misc"]


    while True:
        print("Select a Category: ")
        for i,category in enumerate(expense_categories):
            print(f" {i+1}.{category} ")

        value_range = f"[1 - {len(expense_categories)}]"

        try:
            selected_category_index = int(input(f"Enter a category number {value_range}: ")) - 1
            if selected_category_index in range(len(expense_categories)):
                new_expense = Expense(expense_input, expense_categories[selected_category_index], expense_amount)
                return new_expense
            else:
                print("Invalid Category, Please try again!")

        except ValueError:
            print("Invalid input, Enter an integer value!")

def save_savings_to_file(savings, expense_file):
    print(f"🎯 Saving User Transaction: {savings} to {expense_file}")
    with open(expense_file, "a") as file:
        file.write(f"Income,Income,{savings}\n")

def save_expense_to_file(expense, expense_file):
    print(f"🎯 Saving User Expense: {expense} to {expense_file}")
    with open(expense_file, "a") as file:
        file.write(f"{expense.name},{expense.category},{expense.amount}\n")


def summarize_expenses(expense_file, budget):
    print("🎯 Summarizing User Expense")
    expenses_total = 0
    with open(expense_file, "r") as file:
        next(file)  # Skip the first line
        lines = file.readlines()
        for line in lines:
            expense_name, expense_category, expense_amount = line.strip().split(",")
            if expense_name == "Income":  # Check if the expense is income
                budget += float(expense_amount)  # Add income to the budget
            else:
                expenses_total += float(expense_amount)  # Add expense amount to expenses total
    remaining_budget = budget - expenses_total

    print(f"Total spent: {expenses_total:.2f}")
    print(f"Remaining budget: {remaining_budget:.2f}")

    current_date = datetime.date.today()
    total_days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
    remaining_days = total_days_in_month - current_date.day

    daily_budget = remaining_budget / remaining_days
    print(f"Budget per day: {daily_budget:.2f}")

def prompt_continue():
    while True:
        user_input = input("Do you want to continue? (add/exit): ").lower()
        if user_input == "add":
            return True
        elif user_input == "exit":
            return False
        else:
            print("Invalid input. Please enter 'add' to continue adding expenses or 'exit' to exit the program.")

if __name__ == "__main__":
    main()