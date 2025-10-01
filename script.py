import csv
import pandas as pd
import datetime
from random import randint, choice, choices

# Menu definitions and data structures
menu = { 
    "Milk series": {
        "Plain milk tea": 7.95,
        "Thai milk tea": 8.95,
        "Matcha milk tea": 8.95,
        "Coconut milk tea": 8.95,
        "Brown sugar milk tea": 9.95,
        "Taro milk tea": 9.95
    },
    "Fruit series": {
        "Peach tea": 10.95,
        "Mango tea": 11.95,
        "Lychee tea": 11.95,
        "Taro tea": 10.95
    },
    "Ice blend": {
        "Pina colada": 11.95,
        "Mango slushy": 11.95,
        "Frozen lemonade": 10.95,
        "Matcha ice blend": 10.95
    },
    "Coffee": {
        "Dirty Thai coffee": 8.95,
        "Iced coffee": 7.95
    }
}

toppings = {
    "Pearls (tapioca balls)" : 1.75,
    "Crystal Boba" : 2.50,
    "Lychee Jelly" : 2.75,
    "Passionfruit Jelly" : 2.75,
    "Strawberry Popping Boba" : 2.75,
    "Mango Popping Boba" : 2.75,
    "Pudding" : 1.50,
    "Creama" : 1.00
}

modifications = {
    "sweetness": ['Normal (100%)', 'Less (75%)', 'Half (50%)', 'Light (25%)', 'No Sugar (0%)'],
    "ice": ['Regular', 'Less', 'No Ice'],
}

extras = ["None", "cups", "straws", "napkins", "4 pack cup holder", "bags"]

# Ingredients with stock quantities
ingredients = {
    # Tea bases
    "Black tea leaves": 500,
    "Green tea leaves": 300,
    "Oolong tea leaves": 250,
    "Thai tea mix": 200,
    "Matcha powder": 150,
    "Taro powder": 180,
    "Coffee beans": 400,
    
    # Milk and dairy
    "Whole milk": 1000,
    "Coconut milk": 300,
    "Condensed milk": 250,
    "Heavy cream": 200,
    
    # Syrups and sweeteners
    "Brown sugar syrup": 400,
    "Simple syrup": 500,
    "Honey": 150,
    "Artificial sweetener": 100,
    
    # Fruits and flavoring
    "Peach syrup": 200,
    "Mango puree": 180,
    "Lychee syrup": 150,
    "Pineapple juice": 300,
    "Lemon juice": 250,
    "Passionfruit syrup": 120,
    
    # Toppings ingredients
    "Tapioca pearls (raw)": 800,
    "Crystal boba (raw)": 400,
    "Lychee jelly cubes": 300,
    "Strawberry popping boba": 250,
    "Mango popping boba": 250,
    "Pudding mix": 200,
    "Cream foam powder": 150,
    
    # Supplies
    "Ice": 2000,
    "Plastic cups (16oz)": 1500,
    "Plastic cups (24oz)": 1200,
    "Straws": 2000,
    "Cup lids": 1800,
    "Napkins": 5000
}

# Menu item recipes with ingredient quantities (excluding ice and toppings)
recipes = {
    "Plain milk tea": {"Black tea leaves": 2, "Whole milk": 1, "Simple syrup": 1},
    "Thai milk tea": {"Thai tea mix": 3, "Condensed milk": 1, "Simple syrup": 1},
    "Matcha milk tea": {"Matcha powder": 2, "Whole milk": 1, "Simple syrup": 1},
    "Coconut milk tea": {"Black tea leaves": 2, "Coconut milk": 1, "Simple syrup": 1},
    "Brown sugar milk tea": {"Black tea leaves": 2, "Whole milk": 1, "Brown sugar syrup": 2},
    "Taro milk tea": {"Taro powder": 3, "Whole milk": 1, "Simple syrup": 1},
    "Peach tea": {"Green tea leaves": 2, "Peach syrup": 2, "Simple syrup": 1},
    "Mango tea": {"Green tea leaves": 2, "Mango puree": 3, "Simple syrup": 1},
    "Lychee tea": {"Green tea leaves": 2, "Lychee syrup": 2, "Simple syrup": 1},
    "Taro tea": {"Taro powder": 3, "Simple syrup": 1},
    "Pina colada": {"Pineapple juice": 3, "Coconut milk": 2, "Simple syrup": 1},
    "Mango slushy": {"Mango puree": 4, "Simple syrup": 1},
    "Frozen lemonade": {"Lemon juice": 3, "Simple syrup": 2},
    "Matcha ice blend": {"Matcha powder": 3, "Whole milk": 1, "Simple syrup": 1},
    "Dirty Thai coffee": {"Coffee beans": 2, "Thai tea mix": 1, "Condensed milk": 1},
    "Iced coffee": {"Coffee beans": 2, "Simple syrup": 1}
}

# Data generation parameters
timedelta = 45  # 45 weeks
totalSalesPerDay = 300

# DataFrames for storing generated data
ordersItemsTable = pd.DataFrame(columns=["ItemID", "OrderID", "Drink", "Modifications", "Toppings", "Extras", "Price"])
ordersTable = pd.DataFrame(columns=["OrderID", "Date", "Time", "TotalCost", "EmployeeID", "CustomerID"])
employeeTable = pd.DataFrame(columns=["EmployeeID", "Name", "Role", "PhoneNumber", "Login"])
customerTable = pd.DataFrame(columns=["CustomerID", "Name", "PhoneNumber", "LoyaltyPoints"])

def generate_weighted_date():
    """Generate a date with emphasis on Fridays and Saturdays, and August 25th 2025 as peak day"""
    base_date = datetime.datetime.now()
    days_back = randint(0, timedelta * 7)  # Convert weeks to days
    date = base_date - datetime.timedelta(days=days_back)
    
    # 5% chance to make it August 25th, 2025 (peak day)
    if choice([True] + [False] * 19):  # 5% chance
        return datetime.date(2025, 8, 25)
    
    # If it's not Friday (4) or Saturday (5), give it a chance to be moved to weekend
    if date.weekday() not in [4, 5] and choice([True, False, False]):  # 33% chance to move to weekend
        days_to_weekend = (4 - date.weekday()) % 7  # Days to next Friday
        if choice([True, False]):  # Choose Friday or Saturday
            date = date + datetime.timedelta(days=days_to_weekend)
        else:
            date = date + datetime.timedelta(days=days_to_weekend + 1)
    
    return date.date()

def generate_business_hours():
    """Generate realistic business hours (8 AM - 10 PM)"""
    # Weight hours to favor peak times
    morning_hours = list(range(8, 12))   # 8 AM - 11 AM
    lunch_hours = list(range(12, 15))    # 12 PM - 2 PM  
    afternoon_hours = list(range(15, 18)) # 3 PM - 5 PM
    evening_hours = list(range(18, 22))   # 6 PM - 9 PM
    
    # Weight different time periods
    time_choices = (morning_hours * 2 + lunch_hours * 4 + 
                   afternoon_hours * 3 + evening_hours * 4)
    
    hour = choice(time_choices)
    minute = choice([0, 15, 30, 45])  # Quarter hour intervals for realism
    return datetime.time(hour=hour, minute=minute)

# Create 8 employees
employees = [
    {"EmployeeID": 1, "Name": "Alice Johnson", "Role": "Manager", "PhoneNumber": "5551234101", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 2, "Name": "Bob Smith", "Role": "Cashier", "PhoneNumber": "5551234102", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 3, "Name": "Carol Davis", "Role": "Barista", "PhoneNumber": "5551234103", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 4, "Name": "David Wilson", "Role": "Barista", "PhoneNumber": "5551234104", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 5, "Name": "Emma Brown", "Role": "Cashier", "PhoneNumber": "5551234105", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 6, "Name": "Frank Miller", "Role": "Barista", "PhoneNumber": "5551234106", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 7, "Name": "Grace Lee", "Role": "Assistant Manager", "PhoneNumber": "5551234107", "Login": str(randint(100000, 999999))},
    {"EmployeeID": 8, "Name": "Henry Chen", "Role": "Barista", "PhoneNumber": "5551234108", "Login": str(randint(100000, 999999))}
]

for emp in employees:
    employeeTable.loc[len(employeeTable)] = [emp["EmployeeID"], emp["Name"], emp["Role"], emp["PhoneNumber"], emp["Login"]]

# Generate customers
customer_names = ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson", "Tom Brown", "Lisa Davis", 
                 "Chris Miller", "Amy Taylor", "Steve Garcia", "Maria Rodriguez", "Kevin Lee", "Nancy White",
                 "Paul Anderson", "Linda Thomas", "Mark Jackson", "Susan Martinez", "Robert Harris", "Karen Clark", "James Wilson", "Patricia Lewis", "Michael Young", "Barbara Hall", "William Allen", "Elizabeth King", "David Wright", "Jennifer Scott", "Richard Green", "Maria Adams", "Charles Baker", "Susan Gonzalez", "Joseph Nelson", "Margaret Carter", "Thomas Mitchell", "Dorothy Perez", "Daniel Roberts", "Lisa Turner", "Matthew Phillips", "Nancy Campbell", "Anthony Parker", "Sandra Evans", "Donald Edwards", "Ashley Collins", "Steven Stewart", "Kimberly Sanchez", "Paul Morris", "Donna Rogers", "Andrew Reed", "Michelle Cook", "Joshua Morgan", "Emily Bell", "Ryan Murphy", "Laura Bailey", "Brandon Rivera", "Hannah Cooper", "Justin Richardson", "Megan Cox", "Ethan Howard", "Olivia Ward", "Alexander Torres", "Sophia Peterson", "Jacob Gray", "Isabella Ramirez", "Mason James", "Ava Watson", "Liam Brooks", "Mia Kelly", "Evelyn Sanders", "Elijah Price", "Harper Bennett", "Aiden Wood", "Amelia Barnes", "Logan Ross", "Ella Henderson", "Lucas Coleman", "Scarlett Jenkins", "Jackson Perry", "Victoria Powell", "Sebastian Long", "Aria Patterson", "Jack Hughes", "Grace Flores", "Owen Washington", "Chloe Butler", "Henry Simmons", "Penelope Foster", "Gabriel Gonzales", "Riley Bryant", "Carter Alexander", "Layla Russell", "Wyatt Griffin", "Lillian Diaz", "Jayden Hayes", "Nora Myers", "Dylan Ford", "Zoey Hamilton", "Luke Graham", "Stella Sullivan", "Julian Wallace", "Hazel West", "Levi Cole", "Ellie Jordan", "Isaac Reynolds", "Paisley Fisher", "Anthony Ellis", "Audrey Harrison", "Jaxon Gibson", "Skylar McDonald", "Lincoln Cruz", "Violet Marshall", "Joshua Ortiz", "Claire Gomez", "Christopher Murray", "Lucy Freeman", "Andrew Wells", "Anna Webb", "Theodore Simpson", "Samantha Stevens", "Caleb Tucker", "Allison Porter", "Ryan Hunter", "Ariana Hicks", "Nathan Crawford", "Savannah Henry", "Thomas Boyd", "Genesis Mason", "Aaron Moreno", "Leah Kennedy", "Charles Warren", "Sarah Dixon", "Evan Ramos", "Madison Burns", "Christian Gordon", "Aubrey Shaw", "Jonathan Holmes", "Eleanor Rice", "Connor Robertson", "Natalie Hunt", "Landon Black", "Zoe Daniels", "Brayden Palmer", "Hazel Mills", "Jeremiah Nichols", "Violet Grant", "Cameron Knight", "Aurora Ferguson", "Ezekiel Rose", "Savannah Stone", "Colton Hawkins", "Brooklyn Dunn", "Dominic Perkins", "Claire Hudson", "Ian Spencer", "Skylar Gardner", "Adam Stephens", "Lucy Payne", "Jace Murray", "Paisley Russell", "Robert Sullivan"]

for cust_id, name in enumerate(customer_names, 1):
    phone = f"555123{2000 + cust_id:04d}"
    loyalty_points = randint(0, 500)
    customerTable.loc[len(customerTable)] = [cust_id, name, phone, loyalty_points]

# Generate order data
i = 0
totalCost = 0
orderId = 0
totalPrice = {"Milk series": 262500, "Fruit series": 225000, "Ice blend": 150000, "Coffee": 112500}

while not all(value < 0 for value in totalPrice.values()):
    # Check if this should be a peak day order
    current_date = generate_weighted_date()
    is_peak_day = current_date == datetime.date(2025, 8, 25)
    
    # Increase items per order on peak day
    if is_peak_day:
        itemsPerOrder = choices([2, 3, 4, 5], weights=[2, 3, 3, 2])[0]  # More items on peak day
    else:
        itemsPerOrder = choices([1, 2, 3, 4], weights=[4, 3, 2, 1])[0]  # Normal distribution
    
    itemIds = []
    totalOrderCost = 0
    
    for _ in range(itemsPerOrder):
        # Pick a random category that still has remaining revenue
        available_categories = [cat for cat in menu.keys() if totalPrice[cat] > 0]
        if not available_categories:
            break
            
        drinkCategory = choice(available_categories)
        drink = choice(list(menu[drinkCategory].keys()))
        price = menu[drinkCategory][drink]

        # Allow multiple toppings (0 to 3 random toppings)
        num_toppings = choices([0, 1, 2, 3], weights=[1, 4, 2, 1])[0]
        topping_choices = [choice(list(toppings.keys())) for _ in range(num_toppings)]
        # Remove duplicates and keep order
        seen = set()
        topping_choices = [x for x in topping_choices if not (x in seen or seen.add(x))]            
        if not topping_choices:
            toppingPrice = 0
            toppings_str = "None"
        else:
            toppingPrice = sum(toppings[t] for t in topping_choices if t in toppings)
            toppings_str = ", ".join(topping_choices)
        
        modSweetness = choice(modifications["sweetness"])
        modIce = choice(modifications["ice"])
        modification_str = f"{modSweetness}, {modIce}"
        
        num_extras = randint(0, 2)
        extrasChoice = ", ".join([choice(extras) for _ in range(num_extras)]) if num_extras > 0 else "None"
        
        cost = price + toppingPrice
        totalPrice[drinkCategory] -= cost
        totalCost += cost
        ordersItemsTable.loc[i] = [i, orderId, drink, modification_str, toppings_str, extrasChoice, round(cost, 2)]
        itemIds.append(i)
        totalOrderCost += cost
        i += 1
    
    # Add order to ordersTable
    if itemIds:  # Only add if we have items
        order_date = current_date
        order_time = generate_business_hours()
        
        # Assign employee (weighted towards baristas and cashiers)
        employee_weights = [1, 3, 4, 4, 3, 4, 2, 4]  # Manager less likely, baristas/cashiers more likely
        employee_id = choices(range(1, 9), weights=employee_weights)[0]
        
        # Assign customer (80% chance of having a customer, 20% anonymous)
        customer_id = choice(range(1, len(customerTable) + 1)) if choice([True] * 4 + [False]) else None
        
        # Add loyalty points if customer exists (1 point per dollar spent)
        if customer_id:
            points_earned = int(totalOrderCost)
            customerTable.loc[customer_id - 1, "LoyaltyPoints"] += points_earned
        
        ordersTable.loc[orderId] = [orderId, order_date, order_time, round(totalOrderCost, 2), employee_id, customer_id]
        orderId += 1

# Write all CSV files
print("Generating CSV files...")

# Write ingredients to ingredients.csv
with open('ingredients.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['IngredientId', 'IngredientName', 'Stock', 'Unit'])
    for ingredient_id, (ingredient, stock) in enumerate(ingredients.items(), start=1):
        unit = "units" if "cups" in ingredient.lower() or "straws" in ingredient.lower() or "lids" in ingredient.lower() or "napkins" in ingredient.lower() else "ml/g"
        writer.writerow([ingredient_id, ingredient, stock, unit])

# Write recipes to recipes.csv
with open('recipes.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['MenuItemName', 'IngredientId', 'Quantity'])
    # IngredientId from 0 to len(ingredients)-1, based on order in ingredients dict
    ingredient_list = list(ingredients.keys())
    for menu_item, ingItems in recipes.items():
        for ingredient, quantity in ingItems.items():
            ingredient_Id = ingredient_list.index(ingredient)+1
            writer.writerow([menu_item, ingredient_Id, quantity])

# Write menu items to menu_items.csv
with open('menu_items.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['MenuItemID', 'Type', 'Category', 'Name', 'Price', 'Available'])
    menu_id = 1
    # Drinks
    for category, items in menu.items():
        for name, price in items.items():
            writer.writerow([menu_id, 'Drink', category, name, price, 'Yes'])
            menu_id += 1
    # Toppings
    for name, price in toppings.items():
        writer.writerow([menu_id, 'Topping', '', name, price, 'Yes'])
        menu_id += 1
    # Modifications
    for mod_type, options in modifications.items():
        for option in options:
            writer.writerow([menu_id, 'Modification', mod_type, option, 0, 'Yes'])
            menu_id += 1
    # Extras
    for extra in extras:
        writer.writerow([menu_id, 'Extra', 'Miscellaneous', extra, 0, 'Yes'])
        menu_id += 1

# Write order and customer data to CSV files
ordersItemsTable.to_csv('orders_items.csv', index=False)
ordersTable.to_csv('orders.csv', index=False)
employeeTable.to_csv('employees.csv', index=False)
customerTable.to_csv('customers.csv', index=False)

print(f"Total Cost: ${totalCost}")
print(f"Total Orders: {len(ordersTable)}")
print(f"Total Employees: {len(employeeTable)}")
print(f"Total Customers: {len(customerTable)}")
print("Sample data:")
print(ordersTable.head())
print("\nAll CSV files generated successfully!")
