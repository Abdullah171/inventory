import sqlite3
from typing import Optional
from pydantic import BaseModel
from datetime import date

def create_tables():
        
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()

        # Create Customer table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
                CustomerID INTEGER PRIMARY KEY,
                Name TEXT,
                Phone TEXT,
                Address TEXT,
                Email TEXT
            )
        ''')


        # Create User table for authentication
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                UserID INTEGER PRIMARY KEY,
                Email TEXT UNIQUE NOT NULL,
                PasswordHash TEXT NOT NULL
            )
        ''')

        # Create Category table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Category (
                CategoryID INTEGER PRIMARY KEY,
                Name TEXT,
                Description TEXT
            )
        ''')

        # Create Product table with a foreign key to Category
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                ProductID INTEGER PRIMARY KEY,
                Name TEXT,
                Description TEXT,
                Price REAL,
                QuantityInStock INTEGER,
                CategoryID INTEGER,
                FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID)
            )
        ''')

        # Create Employee table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employee (
                EmployeeID INTEGER PRIMARY KEY,
                Name TEXT,
                Role TEXT,
                Phone TEXT
            )
        ''')

        # Create Orders table with foreign keys to Customer and Employee
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                OrderID INTEGER PRIMARY KEY,
                Date DATE,
                CustomerID INTEGER,
                EmployeeID INTEGER,
                Cost REAL,
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
                FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
            )
        ''')

        # Create OrderDetails table with foreign keys to Orders and Product
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS OrderDetails (
                OrderDetailsID INTEGER PRIMARY KEY,
                OrderID INTEGER,
                ProductID INTEGER,
                Quantity INTEGER,
                Price REAL,
                FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
                FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
            )
        ''')

        # Commit changes and close the connection
        conn.commit()
        conn.close()
        return "Tables Created Successfully"
    except Exception as e:
        return f"Tables Creation Failed {e}"


class UserCreate(BaseModel):
    Email: str
    Password: str

class UserInDB(BaseModel):
    Email: str
    PasswordHash: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# Data model for creating a new customer
class CustomerCreate(BaseModel):
    Name: str
    Phone: str
    Address: str
    Email: str


# Data model for creating a new category
class CategoryCreate(BaseModel):
    Name: str
    Description: str

# Data model for creating a new product
class ProductCreate(BaseModel):
    Name: str
    Description: str
    Price: float
    QuantityInStock: int
    CategoryID: int


# Data model for creating a new employee
class EmployeeCreate(BaseModel):
    Name: str
    Role: str
    Phone: str

# Data model for creating a new order
class OrderCreate(BaseModel):
    Date: date
    CustomerID: int
    EmployeeID: int
    Cost: float

# Data model for creating a new order details
class OrderDetailsCreate(BaseModel):
    OrderID: int
    ProductID: int
    Quantity: int
    Price: float
