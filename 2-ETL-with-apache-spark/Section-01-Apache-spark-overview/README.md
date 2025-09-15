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
