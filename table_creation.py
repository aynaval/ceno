import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("orders.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    customer_name TEXT,
    order_number INTEGER PRIMARY KEY,
    product_name TEXT,
    quantity INTEGER,
    date_of_order TEXT,
    order_status TEXT,
    delivery_date TEXT
)
''')

names = [
    "Alice Johnson", "Michael Smith", "Priya Patel", "Carlos Gomez", "Emily Zhang",
    "Daniel Kim", "Fatima Ali", "James Anderson", "Sophia Nguyen", "Raj Mehta"
]
products = ['Paracetamol 500mg', 'Amoxicillin 250mg', 'Ibuprofen 200mg', 'Cough Syrup', 'Vitamin D3']
statuses = ['Processing', 'Shipped', 'Delivered', 'Delayed']

for i in range(10):
    name = names[i]
    order_num = random.randint(100000, 999999)
    product = random.choice(products)
    quantity = random.randint(1, 5)
    order_date = datetime.now() - timedelta(days=random.randint(1, 10))
    status = random.choice(statuses)
    delivery_date = order_date + timedelta(days=random.randint(2, 7))

    cursor.execute('''
    INSERT OR REPLACE INTO orders (
        customer_name, order_number, product_name, quantity,
        date_of_order, order_status, delivery_date
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        name,
        order_num,
        product,
        quantity,
        order_date.strftime("%Y-%m-%d"),
        status,
        delivery_date.strftime("%Y-%m-%d")
    ))


conn.commit()
conn.close()
print("Database initialized and dummy data inserted.")
