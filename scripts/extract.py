"""
STEP 1: EXTRACT
Fetch data from a public API (JSONPlaceholder - free fake API)
Real world mein yeh Razorpay/Swiggy ka API hoga
"""

import requests
import pandas as pd
import json
import os
from datetime import datetime

def extract_users():
    """API se users data fetch karo"""
    print("Extracting users from API...")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    users = response.json()
    df = pd.DataFrame([{
        'user_id'  : u['id'],
        'name'     : u['name'],
        'email'    : u['email'],
        'city'     : u['address']['city'],
        'company'  : u['company']['name'],
        'extracted_at': datetime.now().isoformat()
    } for u in users])
    print(f"Users extracted: {len(df)}")
    return df

def extract_orders():
    """API se orders data fetch karo"""
    print("Extracting orders from API...")
    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    todos = response.json()
    # Simulate orders from todos
    df = pd.DataFrame([{
        'order_id'    : t['id'],
        'user_id'     : t['userId'],
        'product'     : f"Product_{t['id'] % 5 + 1}",
        'amount'      : round((t['id'] * 137) % 90000 + 1000, 2),
        'status'      : 'completed' if t['completed'] else 'pending',
        'order_date'  : f"2024-{(t['id'] % 12)+1:02d}-{(t['id'] % 28)+1:02d}",
        'extracted_at': datetime.now().isoformat()
    } for t in todos])
    print(f"Orders extracted: {len(df)}")
    return df

def save_raw_data(df, filename):
    """Raw data CSV mein save karo"""
    os.makedirs('data/raw', exist_ok=True)
    path = f"data/raw/{filename}"
    df.to_csv(path, index=False)
    print(f"Saved: {path}")
    return path

if __name__ == "__main__":
    users_df  = extract_users()
    orders_df = extract_orders()
    save_raw_data(users_df,  'raw_users.csv')
    save_raw_data(orders_df, 'raw_orders.csv')
    print("EXTRACT complete!")
