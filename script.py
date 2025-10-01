# Milk series - 14 %
# Plain milk tea
# Thai milk tea
# Matcha milk tea
# Coconut milk tea
# Brown sugar milk tea
# Taro milk tea

# Fruit series
# Peach tea
# Mango tea
# Lychee tea
# Taro tea

# Ice blend
# Pina colada
# Mango slushy
# Frozen lemonade
# Matcha ice blend

# Coffee
# Dirty Thai coffee
# Iced coffee

#create a dict of drinks
timedelta = 45
totalSalesPerDay = 300
menu = { 
    "Milk series": { #roughly $262500 of revenue 
        "Plain milk tea": 7.95,
        "Thai milk tea": 8.95,
        "Matcha milk tea": 8.95,
        "Coconut milk tea": 8.95,
        "Brown sugar milk tea": 9.95,
        "Taro milk tea": 9.95
    },
    "Fruit series": {  #roughly $225000 of revenue
        "Peach tea": 10.95,
        "Mango tea": 11.95,
        "Lychee tea": 11.95,
        "Taro tea": 10.95
    },
    "Ice blend": { #roughly $150000 of revenue  
        "Pina colada": 11.95,
        "Mango slushy": 11.95,
        "Frozen lemonade": 10.95,
        "Matcha ice blend": 10.95
    },
    "Coffee": { #roughly $112500 of revenue 
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

extras = ["None", "cups", "straws", "napkins", "flatware", "to-go boxes", "bags"]

# total orders should sum up to 750000
# data should have at least 39 weeks of sales history
import pandas as pd
import datetime
from random import randint, choice, choices
#dataframe that can hold menu orders items
ordersItemsTable = pd.DataFrame(columns=["ItemID", "Drink", "Modifications", "Toppings", "Extras"])
ordersTable = pd.DataFrame(columns=["OrderID", "Date", "Time", "TotalCost", "ItemIds"])
employeeTable = pd.DataFrame(columns=["EmployeeID", "Name", "Role", "PhoneNumber", "Login"])

def generate_weighted_date():
    """Generate a date with emphasis on Fridays and Saturdays"""
    base_date = datetime.datetime.now()
    days_back = randint(0, timedelta)
    date = base_date - datetime.timedelta(days=days_back)
    
    # If it's not Friday (4) or Saturday (5), give it a chance to be moved to weekend
    if date.weekday() not in [4, 5] and choice([True, False, False]):  # 33% chance to move to weekend
        days_to_weekend = (4 - date.weekday()) % 7  # Days to next Friday
        if choice([True, False]):  # Choose Friday or Saturday
            date = date + datetime.timedelta(days=days_to_weekend)
        else:
            date = date + datetime.timedelta(days=days_to_weekend + 1)
    
    return date.date()

i = 0
totalCost = 0
orderId = 0
totalPrice = {"Milk series": 262500, "Fruit series": 225000, "Ice blend": 150000, "Coffee": 112500}

while not all(value < 0 for value in totalPrice.values()):
    itemsPerOrder = choices([1, 2, 3, 4], weights=[4, 3, 2, 1])[0]  # Weighted choice favoring fewer items
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
        num_toppings = randint(0, 3)
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
        ordersItemsTable.loc[i] = [i, drink, modification_str, toppings_str, extrasChoice]
        itemIds.append(i)
        totalOrderCost += cost
        i += 1
    
    # Add order to ordersTable
    if itemIds:  # Only add if we have items
        order_date = generate_weighted_date()
        order_time = datetime.time(hour=randint(8, 21), minute=randint(0, 59))
        ordersTable.loc[orderId] = [orderId, order_date, order_time, round(totalOrderCost, 2), ','.join(map(str, itemIds))]
        orderId += 1

ordersItemsTable.to_csv('orders_items.csv', index=False)
ordersTable.to_csv('orders.csv', index=False)
print(f"Total Cost: ${totalCost}")
print(f"Total Orders: {len(ordersTable)}")
print("Orders Table:")
print(ordersTable.head())
print("Order Items Table:")
print(ordersItemsTable.head())