# Section 2: Databricks Warehouse Components

---

## ‣ 2.1 Databricks Architecture

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-Databricks-lakehouse-platform/Images/Section1/PIC%205.png" alt="Data Lakehouse Overview" width="500"/>

### 1) High-Level View
Databricks uses a **two-plane architecture**:
- **Control Plane** (managed by Databricks)
- **Compute/Data Plane** (managed by the customer)

This separation gives **security, scalability, and flexibility** — Databricks manages control/metadata, while your **data and compute stay in your cloud** (AWS/Azure/GCP).

---
### 2) Control Plane (Databricks Subscription)

This is fully managed by **Databricks** and contains:

- **Databricks User Interface (UI)**  
  → The web interface (notebooks, jobs, dashboards, repos, MLflow UI).

- **Compute Orchestration**  
  → Databricks manages clusters, jobs, autoscaling, and task scheduling.

- **Unity Catalog**  
  → Centralized **data governance** (who can access what data, audit logs, role-based access, lineage).

- **Queries & Code**  
  → The notebooks, SQL queries, and ML code are stored here.

✅ **Key Point:** The control plane does **not** store your raw data.  
It only contains metadata, governance, and management logic.

---

### 3) Compute Planes (Where code runs)

This is where the **actual compute happens.**  
There are two options:

1. **Classic Compute Plane (Customer Subscription)**  
   - Runs in your cloud account (Azure, AWS, or GCP).  
   - You provision clusters and attach them to your data sources.  
   - You are billed by your cloud provider for these VMs, storage, and networking.  

2. **Serverless Compute Plane (Databricks Subscription)**  
   - Fully managed by Databricks.  
   - You don’t worry about cluster setup, autoscaling, or infrastructure.  
   - Good for interactive queries, BI dashboards, and SQL workloads.  

✅ **Key Difference:**  
- **Classic:** You own the infrastructure.  
- **Serverless:** Databricks owns the infrastructure.
  
---

### 4) Customer Subscription 
This part is in **your cloud account**:

- **Classic Compute Plane** (clusters, VMs)  
- **Workspace Cloud Storage** (Databricks system files: notebooks, logs, libraries)  
- **Customer Resources** (your own data sources, e.g., Azure Data Lake, AWS S3, on-prem databases, etc.)  

✅ **Security Note:** Your raw data **never leaves your subscription** — Databricks only orchestrates access to it.  

---

### 5) Customer Resources (Your Data Layer)
This is **your data layer.** It can include:

- **Cloud Data Lakes** (e.g., S3, ADLS, GCS)  
- **Databases** (SQL Server, PostgreSQL, MongoDB, etc.)  
- **On-prem systems** (via secure connectors)  
- **Data warehouses**  

✅ You control this layer, Databricks just provides the compute and governance.  

---

### 6) Workflow (Example)

1. **User logs in** → via Databricks UI (control plane).  
2. **Creates a cluster/job** → control plane orchestrates it.  
3. **Cluster spins up** → in either your classic compute plane or Databricks’ serverless compute plane.  
4. **Query runs on your data** → data stays in your subscription (customer resources).  
5. **Results returned** → to the UI or dashboards.  
---
### 7) Benefits

- **Security**: data remains in your environment.  
- **Scalability**: autoscaling clusters or serverless.  
- **Governance**: Unity Catalog for consistent access & lineage.  
- **Flexibility**: choose **Classic** or **Serverless** per use case.

---


## 🔹Example Scenario 1: Fraud Detection in Banking with Databricks
---
### Step 1 – User Access
- A data scientist or fraud analyst logs into the **Databricks UI (Control Plane)**.  
- They open a **notebook** to build or run a fraud detection pipeline.  

### Step 2 – Create a Cluster or Use Serverless
- **Option A (Classic Compute Plane):** The bank creates a cluster in its Azure subscription for large-scale ETL and ML training.  
- **Option B (Serverless SQL):** Analysts run **ad-hoc SQL queries** on transaction data for quick fraud reports.  
- Benefit: Run quick queries on dashboards **without waiting for a cluster to boot**.  

### Step 3 – Connect to Data
- Raw data (customer transactions, credit card swipes, ATM withdrawals, online payments) is stored in **Azure Data Lake Storage (ADLS)**.  
- **Unity Catalog** ensures governance:  
  - Analysts can only see **anonymized transaction data**.  
  - Personally Identifiable Information (PII) like names/account numbers is restricted to compliance officers.
 
    
### Step 4 – Run Queries / Code
- A fraud detection model is coded in **PySpark / MLflow** in a Databricks notebook.  
- Example:  

```python
suspicious_txn = transactions_df.filter(
    (transactions_df.amount > 5000) &
    (transactions_df.location != transactions_df.home_location)
)
```   
- The **Control Plane** orchestrates and sends instructions to the **Compute Plane**.  

### Step 5 – Data Processing
- The **Compute Plane** spins up VMs to process millions of daily transactions.  
- The compute pulls transaction data from **ADLS** → processes with Spark.  
- Example processing steps:  
  - Clean raw data (remove duplicates, format timestamps).  
  - Aggregate spending patterns per customer.  
  - Apply ML fraud model (e.g., Random Forest, XGBoost) to flag unusual activity.  
 
### Step 6 – Results
- Results are returned to the **Databricks UI**.  
- Analysts can:  
  - **View flagged transactions** in a notebook.  
  - **Send alerts** to fraud monitoring dashboards (via Databricks SQL or Power BI).  
  - **Store flagged records** in **Delta Lake** for audit and compliance.  

### Step 7 – Storage of Metadata
- The fraud detection **notebooks, queries, and job logs** are stored in **Workspace Cloud Storage**.  
- Governance metadata (e.g., *which analyst accessed fraud data*) is tracked in the **Control Plane (Unity Catalog)**.  



---

## 🔹 Example Scenario 2: Customer Churn Prediction in Banking with Databricks
---
**Example:**  
If a customer’s account has very low activity, lots of complaints, and recently transferred money to another bank, the churn model predicts they may **close their account soon**.  


### Step 1 – User Access
- A data scientist logs into the **Databricks UI (Control Plane)**.  
- They open a **notebook** to explore customer data and build an ML churn model.  

### Step 2 – Create a Cluster or Use Serverless
- **Option A (Classic Compute Plane):** The bank spins up a cluster to train ML models on millions of customer records.  
- **Option B (Serverless SQL):** Analysts run SQL queries to check churn rates by branch or region.  

### Step 3 – Connect to Data
- Raw data is stored in **Azure Data Lake Storage (ADLS)** or databases (Customer Resources).  
- Data includes:  
  - Transaction history  
  - Credit card usage  
  - Loan details  
  - Call center logs / complaints  
  - Customer demographics  

- **Unity Catalog** enforces rules:  
  - Marketing team only sees aggregated data.  
  - Personally Identifiable Information (PII) is masked for analysts.  

### Step 4 – Run Queries / Code
- A churn model is built in **PySpark / MLflow**:  
  - Input features: transaction frequency, average balance, number of complaints.  
  - Target variable: whether the customer left in the last 6 months.  

- **Example:**  

```python
from pyspark.ml.classification import RandomForestClassifier
rf = RandomForestClassifier(featuresCol="features", labelCol="churn_flag")
model = rf.fit(training_data)
predictions = model.transform(test_data)

```  
- The **Control Plane** orchestrates and sends instructions to the **Compute Plane**.  

### Step 5 – Data Processing
- The **Compute Plane** (Classic or Serverless) processes large datasets.  
- Data transformations:  
  - Normalize spending data.  
  - Create customer risk scores.  
  - Train/test ML model on millions of rows.  
- **Example:** Model predicts a **“Churn Probability Score”** for each customer.  

### Step 6 – Results
- Results flow back to the **Databricks UI**.  
- Analysts and managers can:  
  - View churn risk in notebooks.  
  - Create dashboards (Databricks SQL / Power BI) showing **high-risk customers**.  
  - Send alerts to the **CRM system** so customer service can call at-risk customers.  

### Step 7 – Storage of Metadata
- Notebooks, training logs, and models are stored in **Workspace Cloud Storage**.  
- **Unity Catalog** tracks model versions, permissions, and data lineage.  
- Compliance team can audit: *“Which data sources were used to predict churn?”*
  
---

# ‣ 2.2 Databricks Compute

✅ **How Databricks Compute Works in Banking (Fraud Detection Example)**  

1. **You log into Databricks UI (Control Plane).**  
   - *Example:* A fraud analyst logs into Databricks to run a pipeline that checks yesterday’s credit card transactions for anomalies.  

2. **You run a notebook → Control Plane tells the Compute Plane to spin up a cluster.**  
   - *Example:* The analyst runs a PySpark notebook with an ML model that scores transactions for fraud risk, and Databricks triggers compute.  

```python
from pyspark.sql import SparkSession

# create Spark session
spark = SparkSession.builder.appName("BankingExample").getOrCreate()

# read transactions data
df = spark.read.csv("transactions.csv", header=True, inferSchema=True)

# find suspicious transactions
suspicious = df.filter(df.amount > 5000)

suspicious.show()


```

3. **A Driver VM + Worker VMs are created inside your VNet.**  
   - Example: Azure spins up 1 Driver VM (to coordinate) and 6 Worker VMs (to process millions of card transactions in parallel).

4. **Cluster type depends on how it was created:**

   - **All-Purpose Cluster → If created manually (Classic Compute)**
     - Expensive to run  
     - Great for interactive analysis and ad hoc work  

     _Ad hoc work = a simple query or quick analysis that an analyst runs on the spot (like a quick fraud investigation)._  

     **Example:**  
     A data science team keeps a cluster alive all day to interactively test different fraud detection algorithms.  
     _“Show me suspicious big transactions from yesterday.”_

   - **Job Cluster → If created by a job (Classic Compute)**
     - Cheaper to run  
     - Great for repeated production workloads  

     **Example:**  
     At 2:00 a.m., Databricks spins up a **job cluster (Scheduled job)** to scan all previous day’s transactions for fraud, then shuts down.

   - **If serverless was chosen → Databricks spins up compute invisibly**
     - Example: A bank manager opens a fraud dashboard; behind the scenes, a serverless SQL query runs instantly to fetch flagged transactions.

5. **The cluster processes your data, returns results to the UI, then either stays alive (all-purpose) or shuts down (job).**  
   - Example:  
     - In the UI, the analyst sees a fraud report listing 1,250 suspicious transactions with risk scores.  
     - If it was an all-purpose cluster → it remains running so the analyst can query further.  
     - If it was a job cluster → it shuts down automatically after generating the report.
---
# 2.3 Databricks Cluster Configuration


<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-Databricks-lakehouse-platform/Images/Section2/Cluster%20Config.png" alt="Data Lakehouse Overview" width="500"/>

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-Databricks-lakehouse-platform/Images/Section2/config%20pic.png" alt="Data Lakehouse Overview" width="500"/>

---

### 1. Policy
Controls what users are allowed to configure.

**a) Unrestricted**

- **Access**: User can configure **any settings** (cluster size, runtime, autoscaling, etc.).
- **Purpose**: Maximum flexibility for advanced work.
- **Limits**: None by default — you can choose very large/expensive clusters.
- **Risk**:High cost/security risk, so enterprises usually disable this or apply guardrails.
- In enterprises, admins often lock this down for cost/security reasons.

**b) Personal Compute**
 
- This is a **default policy** that creates **lightweight, single-user clusters**.
- It’s designed for **personal use, prototyping, and smaller workloads**. 
- You get **single-user access only** *(the cluster is bound to your account)*.
- It **prevents sharing** or team-wide usage.
- It typically **restricts large instance types** to control costs.

> 💡 **Note:** This is your **own personal sandbox cluster** — **not** meant for production or shared team workloads.

**c) Power User Compute**

- For **experienced users** who need more power than **Personal Compute**.
- **Bigger machines allowed**, but still within **some guardrails** *(not fully open)*.
- **Balances flexibility** with **cost control**.

**d) Shared Compute**

- A **shared cluster** where **multiple people** can attach notebooks.
- **Saves cost** → one cluster instead of many.
- **Risk** → **noisy neighbors** *(one user’s heavy job can slow others down)*.

**e) Legacy Shared Compute**

- An **older version** of **Shared Compute**.
- Still exists in **some workspaces**.
- Usually **replaced by Shared Compute** in most environments.
  
---

### 2. Multi node vs Single node

- **Multi node** = 1 Driver VM + multiple Worker VMs (classic Spark cluster).  
- **Single node** = only the Driver VM (good for small tests or dev).  

---

### 3. Access mode

Defines how users can access the cluster.

**a) Single User** 

- Only **one user** *(the owner)* can attach notebooks.
- Supports **all languages** *(Python, SQL, Scala, R, Java)*.
- Best for **private work, debugging, and experiments**.

**b) Shared** 
- **Multiple users** can attach notebooks to the cluster.
- Supports **Python, Scala, SQL only** *(not R or Java)*.
- Each user runs in an **isolated process** *(safer)*.
- Best for **team collaboration**.

**c) No Isolation Shared** 
- Like **Shared**, but with **no process isolation** *(everyone uses the same login on one machine)*.
- Supports **all languages**.
- **Faster and cheaper**, but **less secure** *(users can interfere with each other)*.
- Used in **low-security** or **testing environments**.
    
---

### 4. Databricks runtime version
- The **software stack** on the cluster = the set of software layers that run together on your cluster (Driver + Worker VMs).  
➡️ **(Spark version + Scala + DB runtime)**

**✦ Apache Spark version**  
- Spark = the big data engine that processes your data across VMs.

**✦ Scala version**  
- Spark itself is **written in Scala** (a JVM language like Java).  
- Even if you write in Python (PySpark) or SQL, under the hood Spark still needs Scala/Java.

**✦ DB Runtime**    
This is Databricks’ “bundle” that includes:
- Spark + Scala version  
- Built-in connectors to cloud storage (Azure, AWS, GCP)  
- Libraries for Delta Lake (transactions, schema enforcement)  
- Security patches and optimizations  

👉 *“What software tools should every VM in my cluster come with by default?”*

**Example configuration:**  

- Choose **Databricks Runtime 11.3 LTS (Scala 2.12, Spark 3.3.0)**  
  - Spark 3.3.0 → lets you process millions of transactions in parallel.  
  - Scala 2.12 → Spark’s native language.  
  - DBR 11.3 → Delta Lake for curated transaction tables with **ACID guarantees**.  
- Optional specialized runtimes:  
  - **Databricks ML Runtime** → TensorFlow, PyTorch, MLflow pre-installed (fraud detection, ML).  
  - **Databricks Genomics Runtime** → optimized for DNA sequencing.  
  - **Databricks Photon Runtime** → includes Photon engine for faster SQL.  

---

### 5. Use Photon Acceleration
- **Photon = Databricks’ high-performance query engine** (written in C++ instead of Java/Scala).  
- Makes SQL queries much faster.  

---

### 6. Worker type
- Defines what kind of **Azure VM** is used for workers.  
- Example: `Standard_DS3_v2` → 14 GB RAM, 4 cores: This means each node (VM) in your cluster will have 4 CPU cores & 14 GB of RAM.
- These are the **machines that crunch data** in parallel.  

**Example:**  
- Query = “SUM of all transactions by region.”  
- Driver splits the work:  
  - Worker 1 → Region A  
  - Worker 2 → Region B  
  - Worker 3 → Region C  
- Driver collects all results → final table.  

---

### 7. Driver type
- Defines the VM for the **Driver node** (the coordinator).  
- Example: same as worker → `DS3_v2 (14 GB RAM, 4 cores)`.  
- Sometimes the Driver is bigger if it has to handle lots of **metadata** (structure, not actual data).  

---

### 8. Autoscaling

**Autoscaling Enabled** 

- Databricks can add more Worker VMs temporarily, then scale back down when load decreases.
- Example:
Normal day = **2M transactions**, Black Friday = **20M transactions** → spike  
Cluster scales from 2 Workers → 8 Workers 
  
**Autoscaling Disabled** ❌
- The cluster will run with a **fixed number of workers** *(whatever you set)*.
- Even if your job is **small** → extra workers **sit idle but still cost money**.
- If your job is **huge** → the cluster may **run slower** or even **fail** if it doesn’t have enough workers.

---

### 9. Terminate after inactivity
- Prevents wasting money.  
- Example: **120 minutes** → if nobody runs a job for 2 hours, cluster shuts down.  

---

### 10. Spot instances (unchecked here)
- Spot = cheaper VMs from Azure’s spare capacity.  
- Cloud providers (AWS, Azure, GCP) sometimes sell **unused capacity** as Spot at a discount.  
- **Downside**: if Azure needs that capacity, they can **take it back** (workers killed).  
- **Risk**: not reliable for production (good for dev/test).  
- **Benefit**: big cost savings.  

---


### 11. Advanced options

**a) Azure Data Lake Storage credential passthrough**
- Configure where **cluster logs** (stdout, stderr, Spark logs) are stored.
- What it does: Lets you use your own Azure AD (Active Directory ) identity to access data in ADLS Gen2 (no need to manually manage keys/secrets).
- When to use: If your company uses Azure AD for permissions, enabling passthrough ensures fine-grained access control (you only see the files you’re allowed to).
- If off: You’d need to set credentials manually (via service principal, keys, or Databricks secrets).


**b) Spark Config** 
This lets you pass custom Spark configurations when the cluster starts.

**Example:**
spark.master local[*, 4]
spark.databricks.cluster.profile singleNode

- `MY_VAR` = simple variable.  
- `MY_OTHER_VAR` = builds on `MY_VAR`.  
- `MY_SECRET_DB_PASSWORD` = securely pulled from **Databricks secrets** (so you don’t hardcode passwords).  

These environment variables can be accessed inside your Spark jobs and notebooks.

**C) Logging** 
- Configure where **cluster logs** (stdout, stderr, Spark logs) are stored.  
- Usually sent to **DBFS** (Databricks File System) or **cloud storage** (S3, ADLS, GCS).  
- Important for **debugging jobs** and for **compliance** (auditing).  

**D) Init Scripts** 
- Scripts that run **automatically** when a cluster starts.  
- Stored in **DBFS**, **cloud storage**, or **workspace files**.  
**Examples:**  
  - Install extra libraries (e.g., custom Python package, system dependency).  
  - Configure environment variables.  
  - Mount external storage.  

