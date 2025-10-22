# Section 1: Spark Structured Streaming 
---
## 1.1 Structured Streaming introduction 
### Problem it Solves
Traditional Spark jobs read a **fixed dataset (batch)**.  
However, many real-world systems (e.g., logs, IoT sensors, clickstreams, payments) produce **never-ending data**.  
Structured Streaming allows you to run the **same DataFrame/Dataset code continuously** on new data as it arrives.

### Mental Model
Think of an **"infinite table"** that keeps getting new rows.  
Your query (`select`, `filter`, `groupBy`, etc.) runs incrementally on just the new rows each time.

### How it Runs
- **Micro-batch (default):** Spark processes new data every N seconds (e.g., every 5s).  
- **(Optional)** Continuous modes exist, but most beginners use micro-batch.

### Core Building Blocks
1. **Source** — Where data comes from (e.g., files in a folder, Kafka, sockets, etc.)  
2. **Transformations** — Your logic (select, filter, joins, aggregations, windows…)  
3. **Sink** — Where results go (console, files, Kafka, tables, etc.)  
4. **Trigger** — When to run each batch  
   **Output Mode** — What to emit each time  
5. **Checkpointing** — How Spark remembers progress for reliable recovery

---

## 1.2 Structured Streaming — Demo

### Read a Stream
- **From files:** Put new files into a folder and Spark treats each new file as “new rows”.  
- **From Kafka:** Subscribe to a topic; Spark tracks Kafka offsets.  
- **From a socket:** Simple text stream for teaching.

### Transform the Data
- Parse JSON, cast types, filter, aggregate, and window by time.

### Write the Results
- Console for visibility while learning.  
- Files/Delta tables for real systems.  
- Kafka for downstream consumers.

### Control the Cadence
- Use `trigger(processingTime="10 seconds")` to run every 10 seconds.  
- Watch micro-batches run in the Spark UI.
