from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
import time

app = FastAPI(
    title="Pharma Order Tracking API",
    description="API for tracking pharmaceutical orders using Customer Name and Order Number.",
    version="1.0.0",
    contact={
        "name": "Pharma Support",
        "email": "support@pharmaapi.com",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()


def fetch_order(customer_name: str, order_number: str):
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()

    cursor.execute('''
    SELECT product_name, order_status, delivery_date
    FROM orders
    WHERE customer_name = ? AND order_number = ?
    ''', (customer_name, order_number))

    row = cursor.fetchone()
    conn.close()

    if row:
        product_name, order_status, delivery_date = row
        return f"The order for {product_name} is currently '{order_status}'. Expected delivery date is {delivery_date}."
    else:
        raise HTTPException(status_code=404, detail="Order not found.")

@app.get("/track-order/",summary="Track Order", tags=["Orders"])
def track_order(customer_name: str = Query(...), order_number: str = Query(...)):

    return {"message": fetch_order(customer_name, order_number)}
