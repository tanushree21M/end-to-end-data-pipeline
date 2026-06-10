"""
STEP 2: TRANSFORM
Raw data clean karo aur business logic apply karo
"""

import pandas as pd
import os
from datetime import datetime

def transform_users(input_path):
    print("Transforming users...")
    df = pd.read_csv(input_path)

    df['name']    = df['name'].str.strip().str.title()
    df['email']   = df['email'].str.strip().str.lower()
    df['city']    = df['city'].str.strip().str.title()
    df['company'] = df['company'].str.strip()
    df = df.drop_duplicates(subset=['email'])
    df = df.dropna(subset=['user_id', 'email'])
    df['transformed_at'] = datetime.now().isoformat()

    print(f"Users after transform: {len(df)}")
    return df

def transform_orders(input_path):
    print("Transforming orders...")
    df = pd.read_csv(input_path)

    df['order_date'] = pd.to_datetime(df['order_date'])
    df['amount']     = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df['status']     = df['status'].str.strip().str.lower()
    df['order_month']= df['order_date'].dt.to_period('M').astype(str)
    df['order_year'] = df['order_date'].dt.year

    df['revenue'] = df.apply(
        lambda r: r['amount'] if r['status'] == 'completed' else 0, axis=1)

    df['amount_category'] = pd.cut(
        df['amount'],
        bins=[0, 10000, 50000, 200000],
        labels=['Low', 'Medium', 'High']
    )
    df['transformed_at'] = datetime.now().isoformat()

    print(f"Orders after transform: {len(df)}")
    return df

def create_summary(orders_df, users_df):
    print("Creating customer summary...")
    merged = orders_df.merge(users_df[['user_id','name','city']], on='user_id', how='left')
    summary = merged.groupby(['user_id','name','city']).agg(
        total_orders   =('order_id',  'count'),
        total_revenue  =('revenue',   'sum'),
        avg_order_value=('amount',    'mean'),
        first_order    =('order_date','min'),
        last_order     =('order_date','max')
    ).round(2).reset_index()

    summary['customer_segment'] = pd.cut(
        summary['total_revenue'],
        bins=[0, 50000, 200000, float('inf')],
        labels=['New', 'Regular', 'Premium']
    )
    return summary

def save_clean_data(df, filename):
    os.makedirs('data/clean', exist_ok=True)
    path = f"data/clean/{filename}"
    df.to_csv(path, index=False)
    print(f"Saved: {path}")
    return path

if __name__ == "__main__":
    users_df   = transform_users('data/raw/raw_users.csv')
    orders_df  = transform_orders('data/raw/raw_orders.csv')
    summary_df = create_summary(orders_df, users_df)

    save_clean_data(users_df,   'clean_users.csv')
    save_clean_data(orders_df,  'clean_orders.csv')
    save_clean_data(summary_df, 'customer_summary.csv')
    print("TRANSFORM complete!")
