CREATE TABLE customers (
    CustomerID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    PhoneNumber INT UNIQUE,
    LoyaltyPoints INT DEFAULT 0
);

CREATE TABLE employees (
    EmployeeID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Role VARCHAR(50),
    PhoneNumber INT UNIQUE,
    Login INT UNIQUE
);

CREATE TABLE ingredients (
    IngredientID SERIAL PRIMARY KEY,
    IngredientName VARCHAR(100),
    Stock INT,
    Unit VARCHAR(20)
);

CREATE TABLE menu_items (
    MenuItemID SERIAL PRIMARY KEY,
    Type VARCHAR(50),
    Category VARCHAR(50),
    Name VARCHAR(100),
    Price DECIMAL(5,2),
    Available BOOLEAN
);

CREATE TABLE order_items (
    ItemID SERIAL PRIMARY KEY,
    OrderID INT REFERENCES orders(OrderID),
    Drink VARCHAR(100),
    Modifications VARCHAR(255),
    Toppings VARCHAR(255),
    Extras VARCHAR(255),
    Price DECIMAL(5,2)
);

CREATE TABLE orders (
    OrderID SERIAL PRIMARY KEY,
    Date DATE,
    Time TIME,
    TotalCost DECIMAL(10,2),
    EmployeeID INT REFERENCES employees(EmployeeID),
    CustomerID INT REFERENCES customers(CustomerID)
);

CREATE TABLE recipes (
    MenuItemName VARCHAR(100),
    IngredientID INT REFERENCES ingredients(IngredientID),
    Quantity INT
);
