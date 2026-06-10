"""
Airflow DAG — End-to-End ETL Pipeline
Yeh DAG roz subah 6 baje chalta hai
Extract → Transform → Load
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
sys.path.append('/opt/airflow/scripts')

from extract   import extract_users, extract_orders, save_raw_data
from transform import transform_users, transform_orders, create_summary, save_clean_data
from load      import load_all

# Default args
default_args = {
    'owner'           : 'tanushree',
    'retries'         : 2,
    'retry_delay'     : timedelta(minutes=5),
    'email_on_failure': True,
}

def run_extract():
    users_df  = extract_users()
    orders_df = extract_orders()
    save_raw_data(users_df,  'raw_users.csv')
    save_raw_data(orders_df, 'raw_orders.csv')

def run_transform():
    users_df   = transform_users('data/raw/raw_users.csv')
    orders_df  = transform_orders('data/raw/raw_orders.csv')
    summary_df = create_summary(orders_df, users_df)
    save_clean_data(users_df,   'clean_users.csv')
    save_clean_data(orders_df,  'clean_orders.csv')
    save_clean_data(summary_df, 'customer_summary.csv')

# DAG define karo
with DAG(
    dag_id          ='e2e_etl_pipeline',
    default_args    =default_args,
    description     ='API → Python → Transform → Load',
    schedule_interval='0 6 * * *',   # Roz subah 6 baje
    start_date      =datetime(2024, 1, 1),
    catchup         =False,
    tags            =['etl', 'production']
) as dag:

    # Task 1: Extract
    extract_task = PythonOperator(
        task_id         ='extract_from_api',
        python_callable =run_extract,
    )

    # Task 2: Transform
    transform_task = PythonOperator(
        task_id         ='transform_data',
        python_callable =run_transform,
    )

    # Task 3: Load
    load_task = PythonOperator(
        task_id         ='load_to_warehouse',
        python_callable =load_all,
    )

    # Task 4: Done notification
    done_task = BashOperator(
        task_id      ='pipeline_complete',
        bash_command ='echo "Pipeline completed at $(date)"',
    )

    # Flow: extract → transform → load → done
    extract_task >> transform_task >> load_task >> done_task
