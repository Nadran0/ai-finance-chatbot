import json, os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {"income": 0, "expenses": []}
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"income": 0, "expenses": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def add_income(amount):
    data = load_data()
    data["income"] = amount
    save_data(data)

def add_expense(name, amount, category):
    data = load_data()
    data["expenses"].append({
        "name": name,
        "amount": amount,
        "category": category
    })
    save_data(data)

def get_summary():
    data = load_data()
    total = sum(e["amount"] for e in data["expenses"])
    savings = data["income"] - total

    category_breakdown = {}
    for e in data["expenses"]:
        category = e.get("category", "Other")
        category_breakdown[category] = category_breakdown.get(category, 0) + e["amount"]

    return data["income"], total, savings, category_breakdown

def calculate_goal(goal, months, savings):
    monthly_required = goal / months
    gap = monthly_required - savings
    return monthly_required, gap


# -------- DELETE EXPENSE --------
def delete_expense(index):
    data = load_data()
    if 0 <= index < len(data["expenses"]):
        data["expenses"].pop(index)
        save_data(data)

# -------- EDIT EXPENSE --------
def edit_expense(index, name, amount, category):
    data = load_data()
    if 0 <= index < len(data["expenses"]):
        data["expenses"][index] = {
            "name": name,
            "amount": amount,
            "category": category
        }
        save_data(data)

# -------- RESET INCOME --------
def reset_income():
    data = load_data()
    data["income"] = 0
    save_data(data)