# Section 2: Apache Spark Overview
---
## 1.1 ETL with Apache Spark   


#### How Spark Fits into ETL

- **Extract** → Use Spark connectors (**JDBC, APIs, file readers**) to ingest raw data.  
- **Transform** → Apply **Spark SQL** or **DataFrame operations** to filter, clean, validate, and enrich data.  
- **Load** → Write the results into **databases, cloud storage, or BI/reporting systems**.  


####  Why It Matters

- Traditional ETL tools (like **Informatica, SSIS, Talend**) often struggle with scale.  
- **Spark ETL pipelines** are faster, scalable, and **cloud-friendly** (Databricks, AWS EMR, Azure Synapse).  
- Supports **batch and streaming ETL**, so you can process both **historical data** and **real-time feeds** in the same framework.

✅ **In short:**  
Apache Spark lets you ingest data into **Bronze (raw)**, refine it into **Silver (clean/enriched)**, and then transform it into **Gold (business-ready)** datasets.  

This makes the data **reliable** and consumable for both **machine learning** and **business reporting**.  

---
## 1.2 Full Summary of Unity Catalog in Azure Databricks

## What is Unity Catalog?

Unity Catalog (UC) is Databricks’ centralized data governance and catalog system. It gives you a single, consistent place to:
- Organize data and AI assets  
- Control access (security & permissions)  
- Audit activity  
- Track lineage (where data comes from and how it’s used)  
- Discover data (search, tagging, documentation)  

It works across all workspaces in a region, so policies and rules apply everywhere consistently.


## Key Features
- **“Define once, secure everywhere”** → one access policy, reused across all workspaces in a region.  
- **ANSI SQL security model** → familiar GRANT/REVOKE syntax for permissions.  
- **Auditing & lineage** → automatic logs of who accessed what, and data flow tracking across all languages.  
- **Data discovery** → search, tags, documentation to find data faster.  
- **System tables** → built-in operational data like audit logs, usage, and lineage queries.  


## The Metastore (Top Container)
- The metastore is the top-level container.  
- Each Databricks account has one metastore per region.  
- All Unity Catalog-enabled workspaces in a region attach to that metastore.  
- It stores metadata (tables, views, volumes, models, functions, permissions) and securable objects.  
- Compared to the old Hive metastore, UC’s metastore is **multi-tenant** and works across workspaces, but still separates data logically by region.  


## Unity Catalog  Object Model 

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/2-ETL-with-apache-spark/Images/3LEVEL.png" alt="Data Lakehouse Overview" width="600"/>

1. **Catalogs (Top level)**  
   - Highest level of organization.  
   - Often represent environments (prod, dev), business domains (finance, HR), or sensitivity levels (public, confidential).  
   - Each catalog usually has its own managed storage location.  
   - Non-data objects like storage credentials and external locations also live at the metastore level alongside catalogs.  

2. **Schemas (Middle level)**  
   - Contain tables, views, volumes, functions, models.  
   - Organize data by project, team, or use case.  

3. **Objects (Lowest level)**  
   - **Tables** → structured data (rows/columns). Managed (UC controls data + storage) or External (UC controls access only).  
   - **Views** → saved queries on tables.  
   - **Volumes** → logical areas in storage for files (structured, semi-structured, unstructured). Managed or External.  
   - **Functions** → saved logic returning values or rows (like SQL UDFs).  
   - **Models** → MLflow AI models, registered as functions.  


## Securable Objects (for Data Access Control)
UC uses special objects to manage how Databricks reaches cloud storage and external systems:

**A. Storage Credentials**  
Long-term authentication keys for cloud storage (e.g., AWS IAM role, Azure Service Principal, GCP Service Account).  
Example: `azure_sp_hr_storage` credential stores a Service Principal for HR data in ADLS.  

**B. External Locations**  
A storage path + credential combo that tells UC where the data lives and which key to use.  
Example: `hr_external_location` → path  
`abfss://hrdata@companydatalake.dfs.core.windows.net/` using the `azure_sp_hr_storage` credential.  
Used for external tables or to assign a managed storage location.  

**C. Connections**  
Saved read-only database logins that let Databricks query external databases directly via Lakehouse Federation.  
Example: `mysql_orders_db` → points to `jdbc:mysql://host:3306/orders` with username/password.  

**D. Service Credentials**  
Secure credentials to connect to external SaaS services or APIs (not just storage).  
Example: `salesforce_api_cred` → stores OAuth token for Salesforce.  

## Admin Roles
- **Account admins** → create metastores, attach workspaces, add users, assign privileges.  
- **Workspace admins** → manage users in a workspace; may inherit metastore privileges.  
- **Metastore admins (optional)** → manage data and storage centrally across multiple workspaces in a region.  


## Permissions & Security
- Uses **ANSI SQL GRANT/REVOKE** (or UI, CLI, REST APIs).  
- **Inheritance**: if you have access at a higher level (catalog), it flows down to schemas and objects.  
- Users must have **USE CATALOG** and **USE SCHEMA** before they can query lower-level objects.  
- UC enforces **least privilege** → users only get the minimum access needed.  
- New workspaces get a **workspace catalog** by default, where all users can experiment.  

## Managed vs. External Data
- **Managed Tables/Volumes** → UC manages data + metadata + storage.  
  - Always **Delta format** for managed tables.  
  - Stored in UC-defined managed locations (at metastore, catalog, or schema level).  

- **External Tables/Volumes** → UC manages only access inside Databricks, but the data’s lifecycle and layout are managed outside (e.g., by your cloud provider or another system).  
  - Supports multiple formats: Delta, Parquet, CSV, JSON, Avro, ORC, Text.  

- **Best practice** → Use Managed unless you need to integrate with external systems or register existing data.  


## Cloud Storage & Data Isolation
- UC uses **External Locations + Storage Credentials** to control access to storage paths.  
- **Managed storage hierarchy**:  
  a. Schema-level location (highest priority)  
  b. Catalog-level location  
  c. Metastore-level location (default)  

This hierarchy ensures organizations can meet compliance requirements:  
- **HIPAA** → healthcare data must remain in secure, HIPAA-compliant storage.  
- **GDPR** → EU customer data must stay in EU-based storage accounts.  
- **PCI DSS** → payment card data must reside in encrypted, access-restricted buckets.  
- **Example**: HR production data required by policy to stay in `s3://mycompany-hr-prod`.  


## Environment Isolation (Workspace-Catalog Binding)
- By default, catalogs are shared across all workspaces in the same metastore.  
- With **workspace-catalog binding**, you can restrict which workspaces see which catalogs.  
  - Example: only the **prod workspace** can access `prod_catalog`.  
- You can also bind storage credentials or external locations to specific workspaces for extra isolation.  


## Setup Steps (Simplified)
1. Attach workspace to a Unity Catalog metastore (automatic in most cases).  
2. Create catalogs and schemas.  
3. Define managed storage locations.  
4. Register external locations if needed.  
5. Grant access to users/groups with least privilege.  

#### Requirements & Support
- **Compute**: Unity Catalog requires Databricks Runtime **11.3 LTS+** (or any SQL Warehouse).  
- **Access Modes**: Clusters must run in **standard or dedicated mode** for UC access.  
- **Formats**: Managed = Delta; External = Delta, Parquet, CSV, JSON, Avro, ORC, Text.  
- **Regions**: Supported in all Databricks regions.  




## 1.3 Views in Databricks

- **View** → Permanent, stored in the metastore.  
  - Survives cluster restarts.  
  - Accessible across sessions and by other users (with permissions).  

- **Temporary View** → Session-scoped.  
  - Exists only while the current notebook/cluster session is running.  
  - Disappears when the session ends.  

- **Global Temporary View** → Shared across all notebooks and sessions on the same cluster.  
  - Still temporary, but stored in a special schema (`global_temp`).  
  - Persists until the cluster shuts down.  

## Project 

https://salmaboukhris.github.io/Databricks-Certified-Data-Engineer-Associate---Preparation/
 
