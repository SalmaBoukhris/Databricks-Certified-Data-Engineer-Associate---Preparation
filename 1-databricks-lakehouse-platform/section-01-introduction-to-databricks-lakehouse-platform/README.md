# Section 1: Introduction to databricks Lakehouse Platform 

# ‣ 1.1 Data Lakehouse Overview


The screenshots used for this section were taken from the [Databricks Certified Data Engineer Associate - Ultimate Prep Course](https://www.udemy.com/course/databricks-certified-data-engineer-associate-ultimate-prep/?couponCode=PMNVD1525) .

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section1/PIC%201.png" alt="Data Lakehouse Overview" width="500"/>
         


##  ‣ Data Warehouse
- **Easy way:** A data warehouse is like a **well-organized library**.  
- Data is **cleaned, structured, and optimized**, so you can ask questions quickly using SQL queries or dashboards.  
- **Examples:** Snowflake, Google BigQuery, Amazon Redshift.  

👉 **Use Case:** Business reporting, dashboards, answering questions like *“How many sales did we have last month?”*

---

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section1/PIC%202.png" alt="Data Lakehouse Overview" width="500"/>



##  ‣ Data Lake
- **Easy way:** A data lake  is like a **big storage pool**where you throw all kinds of data ,raw  (collected directly from a source) ( , messy, structured (tables) or unstructured (videos).
-  Usually in file formats like CSV, JSON, or Parque
-  Imagine a giant “Dropbox” for your company’s raw data.
-   sually stored in cheap cloud storage, but messy to use unless you organize it later.

👉 **Use Case:** Best for storing everything cheaply (good for machine learning, logs, IoT, historical data).


## ‣ Delta Lake
- A storage layer built on top of a data lake.  
- Tech layer on top of data lake.  
- Turns raw data lake into a reliable data lakehouse.  
- Adds:  
  - ACID guarantees (safe writes, consistent reads).  
  - Schema enforcement/evolution.  
  - Time travel (query old versions).  
    Versions are numbered starting at 0:  
    - Version 0 → the table was first created.  
    - Version 1 → after the first update/insert.  
    - Version 2 → after the second update/insert.  
  - Efficient updates & deletes (MERGE INTO).  


## ‣ Delta Table
- A Delta Table is a specific table stored in Delta Lake format.  
- Basically a single organized dataset inside Delta Lake.  
- Under the hood, backed by:  
  - Parquet files → hold the actual rows of data (transactions, customers, etc.).  
  - Delta log (`_delta_log` folder) → stores metadata, schema, version history (for updates, deletes, and time travel).  
- This combination makes Delta Tables ACID-compliant and reliable.  
- It’s the object you query with Spark SQL or PySpark.  

✅ **Example (Banking):**  

A Delta Table `fraud_transactions` might have:  
- Parquet files with all fraudulent transaction rows.  
- A `_delta_log` folder that records changes (e.g., *“row 123 was flagged as fraud yesterday”*).  

Delta log doesn’t track row-level updates directly.  
- It tracks which files are valid at each version.  
- When you query:  
  - Version 0 → Spark reads `part-0000.parquet`.  
  - Version 1 → Spark reads `part-0001.parquet`.  
  - Version 2 → Spark reads `part-0002.parquet`.  
That’s how time travel works — the log tells Spark which Parquet files to use for each version.  


## ‣ Dataset
- A dataset = a collection of data (usually rows + columns).  
- It can live anywhere: in a file, in a database, or in a data lake.  
- Formats: CSV, JSON, Excel, Parquet, etc.  

---

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%203.png" alt="Data Lakehouse Overview" width="500"/>


## ‣ Data Lakehouse
- Easy way: A data lakehouse is like combining the Dropbox (data lake) with the library (data warehouse) in one place.  
- You don’t need to copy data between a messy lake and a structured warehouse — you can store raw + structured data together and still query it fast.  
- Databricks actually invented the Lakehouse concept.  

👉 Use: Machine learning + BI (business intelligence) together, saving time and money.  


### ‣ ACID Rules
ACID = four key rules that make data safe and consistent:

1. **A = Atomicity**  
   - A write either fully happens or doesn’t happen at all.  
   - No “half-written” transactions.  
   - Example: If you’re inserting 1,000 banking transactions and one fails, none are written → table stays clean.  

2. **C = Consistency**  
   - Data always follows rules (schema, constraints).  
   - Example: If `amount_usd` must be a number, Delta Lake won’t allow a string like `"five thousand"`.  
   - Delta Lake = where you save curated (clean, ready) transaction tables.  

3. **I = Isolation**  
   - Multiple jobs can run at the same time without interfering.  
   - Example: Analyst runs a fraud query while a nightly ETL is writing new transactions. Delta ensures both see correct data (no conflict).  

4. **D = Durability**  
   - Once data is written, it’s permanent and safe (survives cluster crashes).  
   - Example: If a cluster fails, yesterday’s fraud results are still there in the Delta table.  
---

# 1.2 Medallion Architecture


<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%204.png" alt="Data Lakehouse Overview" width="500"/>


## ‣ Medallion Architecture
🔹 The standard Lakehouse data flow in Databricks:  
**Bronze → Silver → Gold (Curated)**  

*Curated = cleaned, validated, business-ready (not raw).*

txn_id | customer_id | amount_usd | timestamp | risk_score


### 1. Bronze (Raw Delta)
- **What it is:** Raw ingested data, almost no processing.  
- **Purpose:** Preserve original source in Delta format.  
- **Example in banking:** Daily credit card transaction logs ingested as-is (may have duplicates, missing values, messy timestamps).  
- **Stored as:** `bronze.transactions` (Delta table).  


### 2. Silver (Cleaned Delta)
- **What it is:** Transformed, standardized, deduplicated data.  
- **Purpose:** Make data analytics-ready while keeping detail.  
- **Example in banking:**  
  - Convert all amounts to USD.  
  - Remove duplicate transactions.  
  - Standardize timestamps.  
- **Stored as:** `silver.transactions_clean` (Delta table).  

### 3. Gold (Curated Delta)
- **What it is:** Aggregated, enriched, business-level data.  
- **Purpose:** Directly feed dashboards, reports, ML models.  
- **Example in banking:**  
  - Daily fraud risk scores per customer.  
  - Monthly churn risk predictions.  
  - Regional revenue summaries.  
- **Stored as:** `gold.transactions_curated` (Delta table).  


✅ **Simple takeaway:**  
- Bronze = just landed, raw.  
- Silver = cleaned and standardized.  
- Gold/Curated = polished, business-ready.  

---

# 1.3 Databricks Overview 

### ‣ What is Databricks?
- Databricks is a **company + platform** built on top of Apache Spark.  
- Spark by itself is powerful, but **hard to manage** (installing, configuring, scaling clusters, managing jobs, handling security).  
- Databricks makes Spark **easy to use in the cloud** by adding:  
  - Friendly web interface (notebooks, dashboards, SQL editor).  
  - Cluster management (1-click start/stop).  
  - Data governance (Unity Catalog for security & lineage).  
  - Integrations (Azure, AWS, GCP, Power BI, MLflow).  
  - Serverless compute (no need to manage clusters).  

**Easy way:**  
- Think of Databricks as a **workbench** where data engineers, scientists, and analysts can all work together.  
- Like Google Docs for data → multiple people can clean, process, analyze, and use data in the same platform.  
- Uses Apache Spark under the hood but makes it easier via notebooks, dashboards, and tools.  

👉 **Use:** Build pipelines, run ML, and do analytics in one platform.  

---

### ‣ What is Apache?
- Apache = the **Apache Software Foundation (ASF)**.  
- ASF is a **non-profit** that hosts and maintains **hundreds of open-source projects**.  
- Provides **governance, brand, and community support**.  

Some famous Apache projects:  
- Apache HTTP Server 🌍 (most used web server).  
- Apache Hadoop (big data framework).  
- Apache Kafka (real-time messaging system).  
- Apache Spark (data processing engine).  

👉 Think of Apache as a **parent company** for open-source projects.  

---

### ‣ What is Apache Spark?
- Spark is one of the ASF’s open-source projects.  
- Full name = **Apache Spark**.  
- A **big data processing engine** designed to:  
  - Process huge datasets (TBs / PBs).  
  - Run distributed across clusters.  
  - Support SQL, streaming, ML, and graph analytics.  

👉 Spark = an **open-source technology** under Apache.  

**Example:** Count all words in every book worldwide → Spark splits books across many computers, counts in parallel, merges results.  

---

### ‣ Why Spark Matters
- Traditional systems (SQL DBs, Hadoop MapReduce) = **slow** (step-by-step, writing to disk).  
- Spark keeps data in **memory (RAM)** → **10–100x faster**.  

👉 In short:  
- Spark = the **engine** (raw electricity ⚡).  
- Databricks = the **power company** (packages & delivers it so you can just plug in).  

---

### ‣ Why Spark > Hadoop
### Hadoop
- Speed: Processes from disk → writes results to disk → reads again → **very slow**.  
- Ease of Use: Required **Java code** (complex).  
- Unified Platform: Mainly **batch jobs** (overnight ETL).  
- In-Memory ML: Not built for ML.  

### Spark
- Speed: Processes data **in-memory (RAM)** → up to **100x faster**.  
- Ease of Use: Supports **Python, SQL, Scala, R, Java**.  
- Unified Platform: All-in-one:  
  - Batch (ETL)  
  - Streaming (IoT, Kafka)  
  - ML (MLlib)  
  - Graph analytics (GraphX)  

👉 Example: Hadoop = 3 hrs for 1 TB. Spark = 10 min.  


### ‣ Community & Ecosystem
- Spark became the **most active Apache project**.  
- Used by Netflix, Uber, Facebook, Airbnb, Amazon, etc.  
- Databricks (founded by Spark’s creators) gave Spark a **commercial home** + expanded it with Delta Lake, Unity Catalog, MLflow.  

---

### ‣ Example: Banks & Finance 💳
**Problem:**  
- Billions of transactions daily.  
- Need real-time fraud detection.  

**Solution with Spark/Databricks:**  
- Spark Streaming ingests credit card transactions in real time.  
- ML models detect anomalies (suspicious behavior).  
- Databricks ensures pipelines scale globally & comply with regulations.  

👉 Fraud is prevented **within seconds** of a bad transaction.  

---
# ‣ 1.4 Creating a Databricks Service

    
### Steps
1. Sign in to the **Azure Portal**.  
2. From the **top left menu (3 lines)**, click **Create a resource**.  
3. Search for **Azure Databricks** (black and red logo), then click **Create**.  

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%206.png" alt="Data Lakehouse Overview" width="500"/>



### Configuration
- **Resource group:** Create a new one → `DE-Learning`  
- **Workspace name:** `DE-Learning-WS`  
- **Region:** Canada  
- **Pricing Tier:** Premium


➡️ Click **Next** to continue.  

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%207.png" alt="Data Lakehouse Overview" width="500"/>

---


### Encryption Settings
1. Click **Next**.  
2. **Encryption:** Leave them off.  

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%208.png" alt="Data Lakehouse Overview" width="500"/>

---

### Additional Settings

1. Click **Next** again.  
2. Leave the remaining options off / default.  

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%209.png" alt="Data Lakehouse Overview" width="500"/>


---

### Final Step
1. Click **Review + Create**.  
2. Wait for validation to succeed.  
3. Click **Create**.  

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%2010.png" alt="Data Lakehouse Overview" width="500"/>

---
# ‣ 1.5 Databricks User Interface

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%2011.png" alt="Data Lakehouse Overview" width="500"/>



### Main Navigation (Left Sidebar)
- **New (+)** → Create or upload data, start a new notebook, query, dashboard, job, pipeline, alert, experiment, or model.  
- **Workspace** → Central place to organize notebooks, folders, and shared projects.  
- **Recents** → Quick access to recently opened notebooks, jobs, or dashboards.  
- **Catalog** → Manage access to data (schemas, tables, views) via **Unity Catalog**.  
- **Workflows** → Create and monitor jobs, pipelines, and scheduled tasks.  
- **Compute** → Manage clusters, pools, and resources for Spark workloads.  

---

### SQL Section
- **SQL Editor** → Write SQL queries directly against Delta tables.  
- **Queries** → Save, reuse, and share SQL queries.  
- **Dashboards** → Build visualizations from query results.  
- **Alerts** → Get notified when query conditions are met.  
- **Query History** → Track executed queries for auditing or debugging.  
- **SQL Warehouses** → Provisioned or serverless endpoints for running SQL queries.  

---

### Data Engineering Section
- **Job Runs** → Track execution status and history of scheduled jobs.  
- **Data Ingestion** → Import raw data into the lakehouse for processing.  
- **Delta Live Tables** → Build production-ready data pipelines with built-in reliability and monitoring.  

---

### Machine Learning Section
- **Experiments** → Manage MLflow experiments and track metrics from model training runs.  
- **Features** → Centralized feature store to reuse engineered features across models.  
- **Models** → Register, version, and deploy machine learning models.  

---

### Settings Panel
On the right side, you’ll find:  
- **Appearance** → Light/dark theme.  
- **Identity & Access / Security** → Manage users, roles, and permissions.  
- **Compute / Development / Advanced** → Fine-tune cluster and runtime settings.  
- **User Preferences** → Language, linked accounts, developer settings.  
---

### ‣ The Resource That Was Created

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-databricks-lakehouse-platform/Images/Section%201/PIC%2021.png" alt="Data Lakehouse Overview" width="500"/>

#### ✅ How They Work Together

When you create an **Azure Databricks Workspace**, Azure automatically provisions several resources to make it work:

1. **Virtual Network (workers-vnet)**  
   - Where your Databricks compute (clusters) live.  
   - *Spin-up* = the moment Azure creates and starts the cluster VMs.  
   - When you run Spark code in Databricks:  
     - Driver VM breaks the job into smaller tasks.  
     - Worker VMs process those tasks in parallel.  
     - Driver VM collects the results and shows them in the Databricks UI (browser).  
   - *Example:* Running a churn prediction job → Azure spins up **1 Driver + 4 Worker VMs** inside this vNet to process millions of customer transactions.  

2. **Network Security Group (workers-sg)**  
   - Protects clusters from unwanted traffic.  
   - *Example:* Only traffic from the Databricks Control Plane and your storage account is allowed; random internet traffic cannot access worker VMs.  

3. **Storage Account (dbstorage...)**  
   - Stores notebooks, logs, and libraries (workspace storage).  
   - *Example:* Saving a fraud detection notebook → stored here along with cluster logs from the last run.  

4. **Managed Identity (dbmanagedidentity)**  
   - Allows Databricks to securely access Azure resources (e.g., Storage, Key Vault).  
   - *Example:* Cluster reads data from Azure Data Lake using this identity instead of hardcoding secret keys.  

5. **Access Connector (unity-catalog-access-connector)**  
   - Connects Unity Catalog governance to your Azure data.  
   - *Example:* Junior analyst runs a SQL query → Unity Catalog ensures they see **only anonymized data**, while compliance officers see full details.  

