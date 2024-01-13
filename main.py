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


# Endpoint to retrieve customer details by CustomerID
@app.get("/get_customer/{customer_id}")
async def read_customer(customer_id: int, current_user: UserInDB = Depends(get_current_user)):
    cursor.execute('SELECT * FROM Customer WHERE CustomerID = ?', (customer_id,))
    customer = cursor.fetchone()
    if customer:
        customer_dict = {
            "CustomerID": customer[0],
            "Name": customer[1],
            "Phone": customer[2],
            "Address": customer[3],
            "Email": customer[4],
        }
        return customer_dict
    else:
        raise HTTPException(status_code=404, detail="Customer not found")


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

@app.get("/get_category/{category_id}")
async def read_category(category_id: int, current_user: UserInDB = Depends(get_current_user)):
    cursor.execute('SELECT * FROM Category WHERE CategoryID = ?', (category_id,))
    category = cursor.fetchone()
    if category:
        category_dict = {
            "CategoryID": category[0],
            "Name": category[1],
            "Description": category[2],
        }
        return category_dict
    else:
        raise HTTPException(status_code=404, detail="Category not found")

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

@app.get("/get_product/{product_id}")
async def read_product(product_id: int, current_user: UserInDB = Depends(get_current_user)):
    cursor.execute('SELECT * FROM Product WHERE ProductID = ?', (product_id,))
    product = cursor.fetchone()
    if product:
        product_dict = {
            "ProductID": product[0],
            "Name": product[1],
            "Description": product[2],
            "Price": product[3],
            "QuantityInStock": product[4],
            "CategoryID": product[5],
        }
        return product_dict
    else:
        raise HTTPException(status_code=404, detail="Product not found")


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


@app.get("/get_employee/{employee_id}")
async def read_employee(employee_id: int, current_user: UserInDB = Depends(get_current_user)):
    cursor.execute('SELECT * FROM Employee WHERE EmployeeID = ?', (employee_id,))
    employee = cursor.fetchone()
    if employee:
        employee_dict = {
            "EmployeeID": employee[0],
            "Name": employee[1],
            "Role": employee[2],
            "Phone": employee[3],
        }
        return employee_dict
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

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
    

@app.get("/get_order/{order_id}")
async def read_order(order_id: int, current_user: UserInDB = Depends(get_current_user)):
    cursor.execute('SELECT * FROM Orders WHERE OrderID = ?', (order_id,))
    order = cursor.fetchone()
    if order:
        order_dict = {
            "OrderID": order[0],
            "Date": order[1],
            "CustomerID": order[2],
            "EmployeeID": order[3],
            "Cost": order[4],
        }
        return order_dict
    else:
        raise HTTPException(status_code=404, detail="Order not found")


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

