from fastapi import FastAPI, HTTPException
import sqlite3
from authenticaion import get_password_hash, verify_password, create_access_token, get_current_user
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from datetime import  timedelta
from models import CustomerCreate, UserCreate, Token, UserInDB, create_tables, CategoryCreate, ProductCreate , OrderCreate, OrderDetailsCreate, EmployeeCreate
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield  # This point is where the FastAPI application runs


app = FastAPI(lifespan=lifespan)

# SQLite database connection
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()
# Endpoint to create a new customer



@app.post("/create_customers/")
async def create_customer(customer: CustomerCreate, current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            INSERT INTO Customer (Name, Phone, Address, Email)
            VALUES (?, ?, ?, ?)
        ''', (customer.Name, customer.Phone, customer.Address, customer.Email))
        conn.commit()
        customer_id = cursor.lastrowid
        return {"CustomerID": customer_id, **customer.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/create_category/")
async def create_category(category: CategoryCreate, current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            INSERT INTO Category (Name, Description)
            VALUES (?, ?)
        ''', (category.Name, category.Description))
        conn.commit()
        category_id = cursor.lastrowid
        return {"CategoryID": category_id, **category.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_product/")
async def create_product(product: ProductCreate, current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            INSERT INTO Product (Name, Description, Price, QuantityInStock, CategoryID)
            VALUES (?, ?, ?, ?, ?)
        ''', (product.Name, product.Description, product.Price, product.QuantityInStock, product.CategoryID))
        conn.commit()
        product_id = cursor.lastrowid
        return {"ProductID": product_id, **product.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_employee/")
async def create_employee(employee: EmployeeCreate, current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            INSERT INTO Employee (Name, Role, Phone)
            VALUES (?, ?, ?)
        ''', (employee.Name, employee.Role, employee.Phone))
        conn.commit()
        employee_id = cursor.lastrowid
        return {"EmployeeID": employee_id, **employee.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/create_order/")
async def create_order(order: OrderCreate, current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            INSERT INTO Orders (Date, CustomerID, EmployeeID, Cost)
            VALUES (?, ?, ?, ?)
        ''', (order.Date, order.CustomerID, order.EmployeeID, order.Cost))
        conn.commit()
        order_id = cursor.lastrowid
        return {"OrderID": order_id, **order.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.post("/create_order_details/")
async def create_order_details(order_details: OrderDetailsCreate, current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Price)
            VALUES (?, ?, ?, ?)
        ''', (order_details.OrderID, order_details.ProductID, order_details.Quantity, order_details.Price))
        conn.commit()
        order_details_id = cursor.lastrowid
        return {"OrderDetailsID": order_details_id, **order_details.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@app.get("/customer_info/{customer_id}")
async def get_customer_info(customer_id: int, current_user: UserInDB = Depends(get_current_user)):
    try:
        # Retrieve customer information
        cursor.execute('''
            SELECT * FROM Customer WHERE CustomerID = ?
        ''', (customer_id,))
        customer_data = cursor.fetchone()
        
        if not customer_data:
            raise HTTPException(status_code=404, detail="Customer not found")

        customer_info = {
            "CustomerID": customer_data[0],
            "Name": customer_data[1],
            "Phone": customer_data[2],
            "Address": customer_data[3],
            "Email": customer_data[4]
        }

        # Retrieve customer's orders
        cursor.execute('''
            SELECT * FROM Orders WHERE CustomerID = ?
        ''', (customer_id,))
        orders_data = cursor.fetchall()
        
        orders = []
        for order_data in orders_data:
            order_id = order_data[0]
            order_date = order_data[1]
            employee_id = order_data[3]
            cost = order_data[4]

            # Retrieve employee information for each order
            cursor.execute('''
                SELECT Name, Role, Phone FROM Employee WHERE EmployeeID = ?
            ''', (employee_id,))
            employee_data = cursor.fetchone()
            
            employee_info = {
                "Name": employee_data[0],
                "Role": employee_data[1],
                "Phone": employee_data[2]
            }

            # Retrieve order details for each order
            cursor.execute('''
                SELECT ProductID, Quantity, Price FROM OrderDetails WHERE OrderID = ?
            ''', (order_id,))
            order_details_data = cursor.fetchall()
            
            order_details = []
            for detail_data in order_details_data:
                product_id = detail_data[0]
                quantity = detail_data[1]
                price = detail_data[2]

                # Retrieve product information for each order detail
                cursor.execute('''
                    SELECT Name, Description FROM Product WHERE ProductID = ?
                ''', (product_id,))
                product_data = cursor.fetchone()
                
                product_info = {
                    "ProductID": product_id,
                    "Name": product_data[0],
                    "Description": product_data[1],
                    "Quantity": quantity,
                    "Price": price
                }
                order_details.append(product_info)

            order_info = {
                "OrderID": order_id,
                "Date": order_date,
                "Employee": employee_info,
                "Cost": cost,
                "OrderDetails": order_details
            }
            orders.append(order_info)

        customer_info["Orders"] = orders

        print (customer_info)
        return customer_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/customers/total_spent")
async def get_customers_total_spent(current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            SELECT Customer.CustomerID, Customer.Name, SUM(Orders.Cost) as TotalSpent
            FROM Customer
            JOIN Orders ON Customer.CustomerID = Orders.CustomerID
            GROUP BY Customer.CustomerID
        ''')
        result = cursor.fetchall()
        return {"customers": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/products/top_sales")
async def get_top_sales_products(current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            SELECT Product.ProductID, Product.Name, SUM(OrderDetails.Quantity) as TotalSold
            FROM Product
            JOIN OrderDetails ON Product.ProductID = OrderDetails.ProductID
            GROUP BY Product.ProductID
            ORDER BY TotalSold DESC
            LIMIT 5
        ''')
        result = cursor.fetchall()
        return {"top_products": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/orders/details")
async def get_orders_details(current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            SELECT Orders.OrderID, Customer.Name as CustomerName, Employee.Name as EmployeeName, Orders.Cost
            FROM Orders
            JOIN Customer ON Orders.CustomerID = Customer.CustomerID
            JOIN Employee ON Orders.EmployeeID = Employee.EmployeeID
        ''')
        result = cursor.fetchall()
        return {"orders": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/categories/highest_average_price")
async def get_categories_highest_average_price(current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            SELECT Category.CategoryID, Category.Name, AVG(Product.Price) as AveragePrice
            FROM Category
            JOIN Product ON Category.CategoryID = Product.CategoryID
            GROUP BY Category.CategoryID
            ORDER BY AveragePrice DESC
        ''')
        result = cursor.fetchall()
        return {"categories": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to find out which products are out of stock
@app.get("/products/out_of_stock")
async def get_products_out_of_stock(current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            SELECT ProductID, Name
            FROM Product
            WHERE QuantityInStock = 0
        ''')
        result = cursor.fetchall()
        return {"out_of_stock_products": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get a list of products along with their respective categories
@app.get("/products_with_categories")
async def get_products_with_categories(current_user: UserInDB = Depends(get_current_user)):
    try:
        cursor.execute('''
            SELECT Product.ProductID, Product.Name AS ProductName, Category.Name AS CategoryName
            FROM Product
            JOIN Category ON Product.CategoryID = Category.CategoryID
        ''')
        result = cursor.fetchall()
        return {"products_with_categories": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    




@app.post("/users/")
async def create_user(user: UserCreate):
    
    try:
        hashed_password = get_password_hash(user.Password)
        cursor.execute('''
        INSERT INTO User (Email, PasswordHash)
        VALUES (?, ?)
        ''', (user.Email, hashed_password))
        conn.commit()
        return {"msg": "User created successfully"}
    except Exception as e:
        return f"User Registration Failed {e}"



@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    cursor.execute('SELECT * FROM User WHERE Email = ?', (form_data.username,))
    user = cursor.fetchone()
    if not user or not verify_password(form_data.password, user[2]):
        raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
    headers={"WWW-Authenticate": "Bearer"},
    )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # , expires_delta=access_token_expires
    access_token = create_access_token(
    data={"sub": user[1]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", response_class=HTMLResponse)
async def render_html():
    # Read the HTML file and return it as a response
    with open("templates/login.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/inventory", response_class=HTMLResponse)
async def render_inventory_html():
    # Read the HTML file and return it as a response
    with open("templates/inventory.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

