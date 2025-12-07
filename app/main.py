from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

foods = [
    {"id": 1, "name": "Pizza", "price": 60},
    {"id": 2, "name": "Tacos", "price": 35},
    {"id": 3, "name": "Sandwich", "price": 25},
    {"id": 4, "name": "Drink", "price": 10},
]

orders = []

class OrderItem(BaseModel):
    food_id: int
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request, "foods": foods})


@app.get("/foods")
def get_foods():
    return foods


@app.post("/order")
def create_order(order: Order):
    order_id = len(orders) + 1
    total = 0
    details = []

    for item in order.items:
        food = next((f for f in foods if f["id"] == item.food_id), None)
        if not food:
            return {"error": "Food not found"}

        cost = food["price"] * item.quantity
        total += cost

        details.append({
            "food": food["name"],
            "quantity": item.quantity,
            "cost": cost
        })

    result = {"id": order_id, "details": details, "total": total}
    orders.append(result)
    return result
