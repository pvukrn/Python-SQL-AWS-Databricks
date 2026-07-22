# Data Engineering Utilities

A focused collection of data engineering scripts and SQL views designed for a modern data lake architecture. This repository highlights practical solutions for data compliance, sensitive data masking, data quality gating, and dimensional modeling using AWS and Databricks.

## Tech Stack
* **Languages:** Python, SQL
* **Processing:** PySpark, Databricks (Delta Lake)
* **Cloud Infrastructure:** AWS (S3, Athena)

## Included Files

### 1. `tag_stale_files.py`
**Purpose:** Compliance and Storage Management
An AWS Boto3 (Python) script that scans an S3 bucket and tags objects older than a specified threshold (e.g., 90 days) with an `AuditStatus`. This allows a compliance team to review old files prior to manual or automated deletion, offering a safer alternative to blind lifecycle deletion rules.

### 2. `customer_scd2_merge.sql`
**Purpose:** Dimensional Modeling
A Databricks SQL script implementing Slowly Changing Dimensions (SCD) Type 2. It uses Delta Lake `MERGE` logic to upsert incoming customer data, closing out old records and inserting new active rows to perfectly preserve historical state.

### 3. `pii_utils.py`
**Purpose:** Data Security
A PySpark utility function that dynamically masks Personally Identifiable Information (PII) before it lands in the data lake. It includes methods for hashing sensitive identifiers (like SSNs) using SHA-256 and partially redacting email addresses while keeping the domain intact.

### 4. `dq_daily_checks.sql`
**Purpose:** Data Quality
An AWS Athena SQL view that acts as a simple data quality gate. It scans the previous day's raw transaction data to surface anomalies such as negative amounts, missing account mappings, and exact row duplicates. 

## Usage
* **Python Scripts:** Import the functions from `pii_utils.py` or `tag_stale_files.py` directly into your ETL jobs or Airflow DAGs.
* **SQL:** The Databricks and Athena scripts can be deployed via your CI/CD pipeline or run directly in their respective query editors to establish the required views and merge logic.
