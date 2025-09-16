# Databricks notebook source
# MAGIC %md
# MAGIC # Project : Gizmobox 
# MAGIC ##### 1- Set up a Project
# MAGIC ##### 2- Extract Data from the customers JSON file
# MAGIC ##### A- Querry Single File
# MAGIC ##### B-  Query Muliple JSON files 
# MAGIC ##### C- Select file Metadata
# MAGIC ##### D- Register Files in Unity Catalog using Views 

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1- Set up a Project

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Create a schema 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS landing
# MAGIC         MANAGED LOCATION  'abfss://gizmobox@deacourseextdl.dfs.core.windows.net/landing'
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze
# MAGIC        MANAGED LOCATION  'abfss://gizmobox@deacourseextdl.dfs.core.windows.net/bronze'
# MAGIC CREATE SCHEMA IF NOT EXISTS silver
# MAGIC       MANAGED LOCATION  'abfss://gizmobox@deacourseextdl.dfs.core.windows.net/silver'
# MAGIC CREATE SCHEMA IF NOT EXISTS gold
# MAGIC       MANAGED LOCATION  'abfss://gizmobox@deacourseextdl.dfs.core.windows.net/gold'

# COMMAND ----------

# MAGIC %sql
# MAGIC -- (Re)create catalog
# MAGIC CREATE CATALOG IF NOT EXISTS gizmobox;
# MAGIC
# MAGIC -- Work in this catalog
# MAGIC USE CATALOG gizmobox;
# MAGIC
# MAGIC -- Landing + medallion layers
# MAGIC CREATE SCHEMA IF NOT EXISTS landing;
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze;
# MAGIC CREATE SCHEMA IF NOT EXISTS silver;
# MAGIC CREATE SCHEMA IF NOT EXISTS gold;

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Create a volume 

# COMMAND ----------

# MAGIC %sql
# MAGIC use catalog gizmobox;
# MAGIC use schema landing;
# MAGIC create external volume if not exists operational_data
# MAGIC    LOCATION  'abfss://gizmobox@deacourseextdl.dfs.core.windows.net/landing/operational_data'
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create a Volume inside the landing schema
# MAGIC CREATE VOLUME IF NOT EXISTS landing.operational_data
# MAGIC COMMENT 'Landing area for raw course files (TSV/CSV/JSON etc.)';

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verify the schemas/volume exist
# MAGIC SHOW SCHEMAS IN gizmobox;
# MAGIC SHOW VOLUMES IN gizmobox.landing;

# COMMAND ----------

display(
    dbutils.fs.ls(
        "/Volumes/gizmobox/landing/operational_data"
    )
)

# COMMAND ----------

# MAGIC %sql
# MAGIC LIST '/Volumes/gizmobox/landing/operational_data'

# COMMAND ----------

# MAGIC %sql
# MAGIC LIST '/Volumes/gizmobox/landing/operational_data/addresses/';

# COMMAND ----------

# MAGIC %md
# MAGIC ##### 2- Extract Data from the customers JSON file

# COMMAND ----------

# MAGIC %md
# MAGIC ##### A- Querry Single File
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Extract customers Data- Simple JSON
# MAGIC select * from json.`/Volumes/gizmobox/landing/operational_data/customers/customers_2024_10.json`;
# MAGIC     
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##### B-  Query Muliple JSON files

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query Muliple JSON files after 2024
# MAGIC SELECT * FROM json.`/Volumes/gizmobox/landing/operational_data/customers/customers_2024_*.json`;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Query Muliple JSON all the files in a folder 
# MAGIC SELECT * FROM json.`/Volumes/gizmobox/landing/operational_data/customers/`;

# COMMAND ----------

# MAGIC %md
# MAGIC ##### C- Select file Metadata
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC select input_file_name () as file_path, -- Depreacted from Databricks Runtime 13.3 LTS onwords 
# MAGIC        *
# MAGIC   FROM json.`dbfs:/Volumes/gizmobox/landing/operational_data/customers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC select input_file_name () as file_path, -- Depreacted from Databricks Runtime 13.3 LTS onwords,
# MAGIC        _metafata.file_path,
# MAGIC        *
# MAGIC   FROM json.`dbfs:/Volumes/gizmobox/landing/operational_data/customers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- SQL Warehouse or SQL notebook
# MAGIC SELECT
# MAGIC   _metadata.file_path  AS file_path,   -- ← replacement for input_file_name()
# MAGIC   _metadata            AS file_meta,   -- ← shows the expandable object column
# MAGIC   *
# MAGIC FROM json.`dbfs:/Volumes/gizmobox/landing/operational_data/customers`;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##### D- Register Files in Unity Catalog using Views

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW gizmobox.bronze.v_customers AS
# MAGIC SELECT
# MAGIC   *,                                -- all JSON fields
# MAGIC   _metadata.file_path AS file_path  
# MAGIC FROM json.`dbfs:/Volumes/gizmobox/landing/operational_data/customers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- to see the view 
# MAGIC select * from gizmobox.bronze.v_customers

# COMMAND ----------

# MAGIC %md
# MAGIC ##### _Create a temporary Views_

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW tv_customers AS
# MAGIC SELECT
# MAGIC   *,                                -- all JSON fields
# MAGIC   _metadata.file_path AS file_path  
# MAGIC FROM json.`dbfs:/Volumes/gizmobox/landing/operational_data/customers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- to see the temp view 
# MAGIC select * from tv_customers

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC ##### _Create_ _Global_ _temporary_ _Views_

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE Global TEMPORARY VIEW gtv_customers AS
# MAGIC SELECT
# MAGIC   *,                                -- all JSON fields
# MAGIC   _metadata.file_path AS file_path  
# MAGIC FROM json.`dbfs:/Volumes/gizmobox/landing/operational_data/customers`;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- to see the global view 
# MAGIC select * from global_temp.gtv_customers; 

# COMMAND ----------

# MAGIC %md
# MAGIC