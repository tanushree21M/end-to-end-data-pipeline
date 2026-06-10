# End-to-End Data Engineering Pipeline

A production-style data pipeline: API → Python → Airflow → Data Warehouse → SQL Analytics

## Architecture

```
Public API (JSONPlaceholder)
        ↓
   EXTRACT (Python)
   - Fetch users + orders
   - Save as raw CSV
        ↓
  TRANSFORM (Python + Pandas)
   - Clean & validate data
   - Apply business logic
   - Create aggregations
        ↓
     LOAD (SQLite / Snowflake)
   - dim_users
   - fct_orders
   - dim_customer_summary
        ↓
  ORCHESTRATE (Apache Airflow)
   - Scheduled daily at 6 AM
   - Retry on failure
   - Task dependencies
        ↓
SQL ANALYTICS
   - Revenue reports
   - Customer segments
   - Monthly trends
```

## Project Structure

```
end-to-end-pipeline/
├── dags/
│   └── etl_dag.py          # Airflow DAG
├── scripts/
│   ├── extract.py          # API data extraction
│   ├── transform.py        # Data cleaning + transformation
│   └── load.py             # Load to warehouse
├── sql/
│   └── analytics.sql       # Business analytics queries
├── data/
│   ├── raw/                # Extracted raw data
│   ├── clean/              # Transformed data
│   └── warehouse/          # Final warehouse
└── README.md
```

## Pipeline Steps

| Step | File | What It Does |
|------|------|-------------|
| Extract | scripts/extract.py | Fetches users + orders from API |
| Transform | scripts/transform.py | Cleans, validates, enriches data |
| Load | scripts/load.py | Loads to warehouse, generates report |
| Orchestrate | dags/etl_dag.py | Airflow DAG — daily schedule |
| Analyze | sql/analytics.sql | Business insights queries |

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core scripting |
| Pandas | Data manipulation |
| Apache Airflow | Pipeline orchestration |
| SQLite / Snowflake | Data warehouse |
| SQL | Analytics |
| REST API | Data source |

## How to Run Locally

```bash
# Install dependencies
pip install pandas requests

# Run pipeline step by step
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

## Key Concepts Demonstrated

- End-to-end ELT/ETL pipeline
- REST API data ingestion
- Data cleaning and transformation
- Dimensional modeling (fact + dimension tables)
- Airflow DAG with task dependencies
- Error handling and retries
- Business analytics queries

## Author

**Tanushree Mishra**
Senior Data Engineer | 8+ Years Experience
Python | SQL | Airflow | Snowflake | dbt | AWS | Power BI
