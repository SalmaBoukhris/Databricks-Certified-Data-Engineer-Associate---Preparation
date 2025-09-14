# Section : Introduction to Unity Catalog

---
## ‣ 3.1 unity catalog Object model

<img src="https://raw.githubusercontent.com/SalmaBoukhris/Databricks-Certified-Data-Engineer-Associate---Preparation/refs/heads/main/1-Databricks-lakehouse-platform/Images/Section3/s3p1.png" alt="Data Lakehouse Overview" width="500"/>

### 1) What problem does Unity Catalog solve

Before UC, each Databricks workspace kept its own Hive metastore. That meant:

- duplicate tables and permissions per workspace  
- hard to audit who accessed what  
- messy access to files in cloud storage  

Unity Catalog (UC) is Databricks’ account-level data governance layer. One place to:

- define all data objects (tables, views, functions, files/volumes)  
- secure them with fine-grained permissions (down to columns/rows)  
- audit and track lineage  
- share data across workspaces and even externally (Delta Sharing)  

Think of UC as the **Librarian** for all of your data.  

### 2) Object model 

**Data Storage** (e.g., ADLS/S3/GCS)  
Raw files live here: Parquet, CSV, JSON, images, etc.  

**Unity Catalog (governance and names)**  
UC defines securable objects:

- **Metastore** → one per cloud region, at the account level  
- **Catalog** → top folder (e.g., finance, marketing, sandbox)  
- **Schema** → subfolder inside a catalog (like a database)  
- **Table** → structured dataset (usually Delta format)  
- **View** → saved query (can mask columns/rows for security)  
- **Function** → SQL or Python UDFs you can secure and reuse  
- **Volume** → governed files area for arbitrary data (images, models, etc.)  

**Compute (clusters / SQL warehouses)**  
Your notebooks and SQL run on Spark compute, which checks UC permissions before reading/writing.  

**Users & Apps**  
Humans and jobs submit code/queries. UC ensures only allowed access happens.  

**Three-level name**  
Because of UC, you’ll reference data as:  
`catalog.schema.table` (e.g., `finance.ops.transactions`)  


## ‣ 3.2 Databricks Unity Catalog / Hive Metastore Object Mode

### A) UC vs. the old Hive Metastore (quick compare)

| Topic         | Hive Metastore (old) | Unity Catalog                                                      |
| ------------- | -------------------- | ------------------------------------------------------------------ |
| Scope         | per-workspace        | account-level (shared across workspaces)                           |
| Namespace     | `database.table`     | `catalog.schema.table`                                             |
| Security      | table-level ACLs     | fine-grained (catalog/schema/table/column/row), functions, volumes |
| Files access  | ad-hoc keys, DBFS    | **Storage Credentials** + **External Locations** + **Volumes**     |
| Audit/Lineage | limited              | built-in lineage + audit logs                                      |
| Sharing       | manual copies        | **Delta Sharing** (cross-workspace/org)                            |


### B) Key Objects Inside Unity Catalog

| Object    | What it is (in plain English)                                              |
| --------- | -------------------------------------------------------------------------- |
| Metastore | Master library building. One per cloud region.                             |
| Catalog   | Top-level folder for data (like a department).                             |
| Schema    | Sub-folder inside catalog (like a database).                               |
| Table     | Structured dataset (usually Delta format).                                 |
| View      | A saved query (often used for masking sensitive data).                     |
| Function  | A reusable formula or custom function.                                     |
| Volume    | Governed area for arbitrary files (CSV, images, models).                   |


### C) How UC Connects to Cloud Storage

UC does not store data itself. Data lives in your cloud storage (ADLS, S3, GCS).  
UC uses these concepts:

- **Storage Credential** → secure way to store access keys/identities.  
- **External Location** → pointer to a folder in cloud storage (with a credential).  
- **Managed Location** → default place UC puts files for managed tables.  

👉 You don’t give raw storage keys to every user — UC controls access.

### D) Managed vs External Tables

**Managed table**  
- UC controls the storage path (under the catalog/schema’s *managed storage*).  
- `DROP TABLE` deletes the table’s files.  
- Easiest lifecycle/governance; great for **new curated datasets**.  

**External table**  
- You point UC at an existing path (data may be written by other tools).  
- `DROP TABLE` removes only metadata; files remain.  
- Best when reusing **existing lake paths**, or when other systems also read/write.  

**Rule of thumb:**  
Use **managed** for new projects you fully govern in UC; use **external** when you must keep data in an existing path or share it with non-UC producers/consumers.  



**How UC decides the type**  
- No `LOCATION` in `CREATE TABLE` → **Managed** (files go to the schema/catalog managed location).  
- `LOCATION '…'` provided → **External**.  

## 3.3 Create and Configure a Unity Catalog Metastore

#### Step 1 – Create the Metastore
- Go to the **Databricks Admin Console** (only account admins can do this).  
- In the left menu, select **Catalog → Metastores → Create Metastore**.  
- Enter the following:  
  - **Name**: Give your metastore a name (e.g., `main-metastore`).  
  - **Region**: Select the same cloud region as your Databricks workspace.  
  - **ADLS Gen2 path**: Leave this blank (optional).  
  - **Access Connector ID**: Provide the Azure Databricks access connector if required.  

#### Step 2 – Assign the Metastore to a Workspace
- Still in the Admin Console, go to **Workspaces**.  
- Select the workspace you want to connect.  
- Click **Assign Metastore** and choose the one you just created.  
- Confirm the assignment.  

#### Step 3 – Verify Cluster Configuration
When creating or editing clusters that will use Unity Catalog, make sure:  
- **Runtime**: Use a Databricks Runtime that supports Unity Catalog (**11.3 or higher**).  
- **Access Mode**: Choose **Single User** or **Shared** (not *No Isolation*).  
- **Credential Passthrough**: Keep this **disabled**.  


