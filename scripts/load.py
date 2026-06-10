"""
STEP 3: LOAD
Clean data ko Snowflake mein load karo
(Yahan SQLite use karenge demo ke liye — same concept)
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

def load_to_database(df, table_name, conn):
    """DataFrame ko database table mein load karo"""
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table_name}", conn)
    print(f"Loaded {count['cnt'][0]} rows into {table_name}")

def load_all():
    print("Loading data to database...")

    os.makedirs('data/warehouse', exist_ok=True)
    conn = sqlite3.connect('data/warehouse/data_warehouse.db')

    users_df   = pd.read_csv('data/clean/clean_users.csv')
    orders_df  = pd.read_csv('data/clean/clean_orders.csv')
    summary_df = pd.read_csv('data/clean/customer_summary.csv')

    load_to_database(users_df,   'dim_users',            conn)
    load_to_database(orders_df,  'fct_orders',           conn)
    load_to_database(summary_df, 'dim_customer_summary', conn)

    # Quick report
    print("\n--- PIPELINE REPORT ---")
    report = pd.read_sql("""
        SELECT
            COUNT(*)          AS total_orders,
            SUM(revenue)      AS total_revenue,
            AVG(amount)       AS avg_order_value,
            COUNT(CASE WHEN status='completed' THEN 1 END) AS completed,
            COUNT(CASE WHEN status='pending'   THEN 1 END) AS pending
        FROM fct_orders
    """, conn)
    print(report.to_string(index=False))

    conn.close()
    print("\nLOAD complete!")

if __name__ == "__main__":
    load_all()
