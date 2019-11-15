# CZ4031-PostgresqlQuery-Description

## About

The PostgresqlQuery Descriptor is a desk top application built using python with tkinter library. This project aims to provide an algorithm to describe the Query Eexecution Plan (QEP) generated for each query, draw the QEP as a tree structure, describe the difference in QEPs of similar queries and generate the reason of the changing of the QEP.

This project's purpose is to enhance the beginner's learning expereience of realtional database management systems. Through the visualizing the QEP by both text format and tree structure formate, the learner will be albe to get the idea of QEP easier. By providing the difference of the QEP for 2 similari queries and providing the reason of the changes, the learner will be able to have a good understanding of how a optimized QEP is generated.


## Usage

To use this application, you need to run the app/app.py in this project.

Before running this application, you need to satisfy the following dependencies

### Postgresql Setup

If you don't have a postgresql server or a tpch database, please use the initdb.sql inside the initdb/ directory to create and initialize a tpch database.

Databse sechemas can be also found in initdb.sql

### Dependencies

This application was built with Python v3.6.5 and uses the dependencies specified in `requirements.txt`. Use the command `pip install -r requirements.txt` to install the latest version of the listed packages.

**Note: We use tkinter module to build the GUI and this module should be a built in library. Therefore, no need to install it manually**

### Run script

To run the application, go to your terminal and type:
```bash
python3 app/app.py --host <host> --port <port> --database <db_name> --user <username> --password <password>
```
example
```bash
python3 app/app.py --host localhost --port 5432 --database tpch_db --user eric --password ""
```

The flags are used to connect to postgresql server.

**Note: We recommend to use the full screen mode**

### User Maunal

The application (or system) accept two inputs, namely, two SQL queries.

1. Paste the first query of `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON) <query>` to the first text field. By running the input, the Postgresql can generate the QEP of the first query.

2. Paste the second query of `EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON) <query>` to the first text field. By running the input, the Postgresql can generate the QEP of the second query.

After inserting the two required input, click **"View Output"** to see the result

The output of this system contains 4 parts:
1. The natural language description of the two QEPs

2. The tree structure of the two QEPs

3. The difference between the two QEP, if these two queries's execution plans are comparable

4. The reason of the differerence, if any

### Sample Queries

There are 6 set of sample test queries available in this project.

To use the sample queries, for example, query_1, simply go to the directory queries/query_1. Then you will see query_1a.sql and query_1b.sql

The sql script is inside the file, simply copy that as your input to the system. For example, copy query in query_1a.sql as the old query and the query in query_1b.sql as the new query.

### Example

#### Input
1. First Query

```sql
explain (analyze, costs, verbose, buffers, format json) select *
from nation, region
where nation.regionkey = region.regionkey and nation.nationkey >= 15;
```

2. Second Query

```sql
explain (analyze, costs, verbose, buffers, format json) select *
from nation, region
where nation.regionkey = region.regionkey and region.regionkey = 1;
```

#### Output(Result)

1. Natural Language Description

Description of Query A
```
The query is executed as follow.
Step 1, perform sequential scan on table region.
Step 2, perform sequential scan on table nation and filtering on nation.nationkey >= 15 to get intermediate table T1.
Step 3, hash table T1 and perform hash join on table region and table T1 under condition region.regionkey = nation.regionkey to get the final result.
```

Description of Query B
```
The query is executed as follow.
Step 1, perform sequential scan on table nation and filtering on nation.regionkey = 1 to get intermediate table T1.
Step 2, perform index scan on table region with index region_pkey.
Step 3, perform nested loop on table T1, and table region with index region_pkey to get the final result.
```

2. Tree Structure Description

Tree Structure of QEP of Query A
```
`-- Hash Join
   |-- Seq Scan
   `-- Hash
      `-- Seq Scan
```

Tree Structure of QEP of Query B
```
`-- Nested Loop
   |-- Seq Scan
   `-- Index Scan
```

3. Description of the Difference

```
Difference 1 : hash table T1 and hash join on table region and table T1 under condition region.regionkey = nation.regionkey to get intermediate table T2 has been changed to nested loop on table T1, and table region with index region_pkey to get intermediate table T2

Difference 2 : sequential scan on table nation and filtering on nation.nationkey >= 15 to get intermediate table T1 has been changed to index scan on table region with index region_pkey
```

4. Explanation

```
Reason for Difference 1: Hash Join in P1 on has now evolved to Nested Loop in P2 on relation . This is because the actual row number decreases from 10 to 5. 

Reason for Difference 2: Sequential Scan in P1 on relation nation has now evolved to Index Scan in P2 on relation region. This is because P2 uses the index, i.e. region_pkey, for selection while P1 doesn't. and the actual row number decreases from 10 to 1. This may be due to the selection predicate changes from (nation.nationkey >= 15) to (region.regionkey = 1). 
```

The output actually is the combination of the difference and its explanation
```
Difference 1 : hash table T1 and hash join on table region and table T1 under condition region.regionkey = nation.regionkey to get intermediate table T2 has been changed to nested loop on table T1, and table region with index region_pkey to get intermediate table T2

Reason for Difference 1: Hash Join in P1 on has now evolved to Nested Loop in P2 on relation . This is because the actual row number decreases from 10 to 5. 


Difference 2 : sequential scan on table nation and filtering on nation.nationkey >= 15 to get intermediate table T1 has been changed to index scan on table region with index region_pkey

Reason for Difference 2: Sequential Scan in P1 on relation nation has now evolved to Index Scan in P2 on relation region. This is because P2 uses the index, i.e. region_pkey, for selection while P1 doesn't. and the actual row number decreases from 10 to 1. This may be due to the selection predicate changes from (nation.nationkey >= 15) to (region.regionkey = 1). 
```

## Report

Report is **CZ4031Project2Report.pdf**, which is inside the root directory of this projcet.