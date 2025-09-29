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
timedelta = 39
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
    "None": 0.00,
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
from random import randint, choice
#dataframe that can hold menu orders items
ordersItemsTable = pd.DataFrame(columns=["ItemID", "Drink", "Modifications", "Toppings", "Extras"])

i = 0
totalCost = 0
totalPrice = {"Milk series": 262500, "Fruit series": 225000, "Ice blend": 150000, "Coffee": 112500}
while not all(value < 0 for value in totalPrice.values()):
    for drinkCategory in menu.keys():
        if totalPrice[drinkCategory] > 0: 
            drink = choice(list(menu[drinkCategory].keys()))
            price = menu[drinkCategory][drink]
            
            toppingChoice = choice(list(toppings.keys()))
            toppingPrice = toppings[toppingChoice]
            
            modSweetness = choice(modifications["sweetness"])
            modIce = choice(modifications["ice"])
            modification_str = f"{modSweetness}, {modIce}"
            
            extrasChoice = choice(extras)
            
            cost = price + toppingPrice
            totalPrice[drinkCategory] -= cost
            totalCost += cost
            ordersItemsTable.loc[i] = [i, drink, modification_str, toppingChoice, extrasChoice]
            i += 1
ordersItemsTable.to_csv('orders_items.csv', index=False)
print(totalCost)
print(ordersItemsTable)