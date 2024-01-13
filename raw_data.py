import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Insert data into the Customer table
customer_data = [
    (1, 'John Doe', '123-456-7890', '123 Main St', 'johndoe@email.com'),
    (2, 'Alice Smith', '987-654-3210', '456 Elm St', 'alicesmith@email.com'),
    (3, 'Bob Johnson', '555-123-4567', '789 Oak St', 'bobjohnson@email.com'),
    (4, 'Emily Davis', '777-888-9999', '101 Pine St', 'emilydavis@email.com'),
    (5, 'Michael Wilson', '111-222-3333', '202 Maple St', 'michaelwilson@email.com'),
    (6, 'Sophia Lee', '333-444-5555', '303 Birch St', 'sophialee@email.com'),
    (7, 'William Brown', '222-333-4444', '404 Cedar St', 'williambrown@email.com'),
    (8, 'Olivia White', '444-555-6666', '505 Spruce St', 'oliviawhite@email.com'),
    (9, 'James Miller', '666-777-8888', '606 Redwood St', 'jamesmiller@email.com'),
    (10, 'Ella Martinez', '888-999-0000', '707 Sequoia St', 'ellamartinez@email.com')
]

cursor.executemany('''
    INSERT INTO Customer (CustomerID, Name, Phone, Address, Email)
    VALUES (?, ?, ?, ?, ?)
''', customer_data)

# Insert data into the Category table
category_data = [
    (1, 'Electronics', 'Electronic gadgets and devices'),
    (2, 'Clothing', 'Fashion and apparel'),
    (3, 'Home Decor', 'Home decoration items'),
    (4, 'Books', 'Books and reading materials'),
    (5, 'Toys', 'Children\'s toys'),
    (6, 'Furniture', 'Furniture and home furnishings'),
    (7, 'Sports', 'Sports equipment and gear'),
    (8, 'Beauty', 'Beauty and cosmetics'),
    (9, 'Jewelry', 'Jewelry and accessories'),
    (10, 'Food', 'Food and groceries')
]

cursor.executemany('''
    INSERT INTO Category (CategoryID, Name, Description)
    VALUES (?, ?, ?)
''', category_data)

# Insert data into the Product table
product_data = [
    (1, 'Smartphone', 'Latest smartphone model', 599.99, 100, 1),
    (2, 'T-Shirt', 'Cotton t-shirt in various colors', 19.99, 200, 2),
    (3, 'Table Lamp', 'Modern table lamp with LED', 49.99, 50, 3),
    (4, 'Novel', 'Bestselling novel', 12.99, 150, 4),
    (5, 'Toy Car', 'Remote-controlled toy car', 29.99, 80, 5),
    (6, 'Sofa', 'Comfortable living room sofa', 499.99, 30, 6),
    (7, 'Basketball', 'Official size basketball', 19.99, 40, 7),
    (8, 'Lipstick', 'High-quality lipstick', 9.99, 100, 8),
    (9, 'Necklace', 'Silver pendant necklace', 59.99, 60, 9),
    (10, 'Cereal', 'Breakfast cereal', 4.99, 120, 10)
]

cursor.executemany('''
    INSERT INTO Product (ProductID, Name, Description, Price, QuantityInStock, CategoryID)
    VALUES (?, ?, ?, ?, ?, ?)
''', product_data)

# Insert data into the Employee table
employee_data = [
    (1, 'Sarah Johnson', 'Manager', '555-123-7890'),
    (2, 'David Smith', 'Sales Associate', '555-987-6543'),
    (3, 'Jennifer Davis', 'Cashier', '555-333-2222'),
    (4, 'Robert Brown', 'Warehouse Manager', '555-444-5555'),
    (5, 'Karen Wilson', 'Store Clerk', '555-777-8888'),
    (6, 'Michael Lee', 'Security Guard', '555-222-1111'),
    (7, 'Emily Martinez', 'Customer Service', '555-999-3333'),
    (8, 'Daniel White', 'Inventory Manager', '555-111-6666'),
    (9, 'Jessica Miller', 'Assistant Manager', '555-888-4444'),
    (10, 'Matthew Johnson', 'Janitor', '555-666-2222')
]

cursor.executemany('''
    INSERT INTO Employee (EmployeeID, Name, Role, Phone)
    VALUES (?, ?, ?, ?)
''', employee_data)

# Insert data into the Orders table
orders_data = [
    (1, '2023-01-01', 1, 1, 199.99),
    (2, '2023-01-02', 2, 2, 79.98),
    (3, '2023-01-03', 3, 3, 149.97),
    (4, '2023-01-04', 4, 4, 239.96),
    (5, '2023-01-05', 5, 5, 129.95),
    (6, '2023-01-06', 6, 6, 69.94),
    (7, '2023-01-07', 7, 7, 99.93),
    (8, '2023-01-08', 8, 8, 189.92),
    (9, '2023-01-09', 9, 9, 59.91),
    (10, '2023-01-10', 10, 10, 119.90)
]

cursor.executemany('''
    INSERT INTO Orders (OrderID, Date, CustomerID, EmployeeID, Cost)
    VALUES (?, ?, ?, ?, ?)
''', orders_data)

# Insert data into the OrderDetails table
order_details_data = [
    (1, 1, 1, 599.99),
    (2, 2, 4, 79.98),
    (3, 3, 3, 149.97),
    (4, 4, 2, 119.98),
    (5, 5, 5, 129.95),
    (6, 6, 1, 69.94),
    (7, 7, 2, 49.98),
    (8, 8, 4, 189.92),
    (9, 9, 1, 59.91),
    (10, 10, 3, 359.70)
]

cursor.executemany('''
    INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Price)
    VALUES (?, ?, ?, ?)
''', order_details_data)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully!")
