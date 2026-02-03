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

## 1.2 Spark Structured Streaming — Detailed Notes

###  1. Processing Modes

Spark Structured Streaming supports **two processing modes** — basically two ways it handles streaming data in real time.

| Mode | Description | Behavior |
|------|--------------|-----------|
| **Micro-Batch Processing (Default)** | Spark processes streaming data in **small batches** at regular intervals (e.g., every few seconds). | Spark collects new data → runs your transformations → writes the result → waits for the next trigger. Think of it like “mini batch jobs” running repeatedly. |
| **Continuous Processing (Experimental)** | Spark tries to process **each record as soon as it arrives**, instead of waiting for a batch interval. | This mode aims for **ultra-low latency** (milliseconds), but it’s still **experimental** and supports only limited sinks (like Kafka). |

###### 🔹 Example for Micro-Batch (Default)

```python
query = df.writeStream.trigger(processingTime="5 seconds").start()
```
---
### 2.  Triggers — “When” Spark Runs Each Batch

A **trigger** defines *when* and *how often* Spark should check for new data and run a micro-batch.

| **Trigger Type** | **Trigger Syntax** | **Description** |
|------------------|--------------------|-----------------|
| **Default (No Trigger)** | *(No trigger specified)* | Spark automatically runs micro-batches every ~500 milliseconds (very fast) — not often used in production. |
| **Fixed Interval** | `.trigger(processingTime="2 minutes")` | Spark runs a micro-batch every 2 minutes — this is the most common trigger type. |
| **Triggered Once** | `.trigger(once=True)` | Spark processes all available data once, writes output, then stops (useful for one-time backfill jobs; now deprecated). |
| **Available Now** | `.trigger(availableNow=True)` | Spark processes all current data (could take multiple micro-batches), then stops — commonly used to catch up historical data. |
| **Continuous** | `.trigger(continuous="2 seconds")` | Spark processes data continuously, committing checkpoints every 2 seconds. ⚠️ *This is experimental.* |


###### How to Think About Triggers

Imagine a **security camera** that captures new footage every few seconds:

- 🎞️ **Default Trigger:** Takes a snapshot every 0.5 second — super fast.  
- ⏲️ **Fixed Interval (5 seconds):** Captures new video clips every 5 seconds.  
- 📸 **Once:** Takes one snapshot and turns off.  
- 🧭 **AvailableNow:** Captures everything available now, then stops.  
- 🔁 **Continuous:** Keeps recording live feed, never stops *(but still experimental)*.

---

### 3. Output Modes — “What” Spark Writes Each Time

After Spark processes a micro-batch, it must decide **what part of the results** to send to the sink (destination).  
This is controlled by the **output mode**.

| **Output Mode** | **Description** | **Use Case** |
|-----------------|-----------------|---------------|
| **Append (Default)** | Writes **only the new rows** since the last micro-batch. | Simple streams with no aggregations (like logs, sensor readings). |
| **Complete** | Writes the **entire result table** each time (overwrites previous output). | Small aggregations or console output — good for debugging. |
| **Update** | Writes **only the rows that have changed** since the last micro-batch. | Aggregations or stateful computations that update over time. |


##### Example Query

```python
query = (spark.readStream
               .format("json")
               .load("/incoming")
               .groupBy("category")
               .count()
               .writeStream
               .outputMode("update")             # what to write
               .trigger(processingTime="10 s")   # when to run
               .option("checkpointLocation", "/chk/category_counts")
               .format("console")                # where to write
               .start())
```

# Section 2: Auto Loader  
