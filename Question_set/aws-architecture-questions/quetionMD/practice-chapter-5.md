# Solutions Architect Ch5: Database Services

1. In a relational database, a row may also be called what? (Choose two.)
    - A. Record.
    - B. Attribute.
    - C. Tuple.
    - D. Table.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: Different relational databases use different terminology. A row, record, and tuple all
    </details>

2. What must every relational database table contain?
    - A. A foreign key.
    - B. A primary key.
    - C. An attribute.
    - D. A row.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: A table must contain at least one attribute or column. Primary and foreign keys are used
    </details>

3. Which SQL statement would you use to retrieve data from a relational database table?
    - A. QUERY.
    - B. SCAN.
    - C. INSERT.
    - D. SELECT.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The SELECT statement retrieves data from a table. INSERT is used for adding data to
    </details>

4. Which relational database type is optimized to handle multiple transactions per second?
    - A. Offline transaction processing (OLTP).
    - B. Online transaction processing (OLTP).
    - C. Online analytic processing (OLAP).
    - D. Key/value store.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Online transaction processing databases are designed to handle multiple transactions per
    </details>

5. How many database engines can an RDS database instance run?
    - A. Six.
    - B. One.
    - C. Two.
    - D. Four.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Although there are six database engines to choose from, a single database instance can run
    </details>

6. Which database engines are compatible with existing MySQL databases? (Choose all that apply.)
    - A. Microsoft SQL Server.
    - B. MariaDB.
    - C. Aurora.
    - D. PostgreSQL.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: MariaDB and Aurora are designed as binary drop- in replacements for MySQL. Post-
    </details>

7. Which storage engine should you use with MySQL, Aurora, and MariaDB for maximum compatibility with RDS?
    - A. MyISAM.
    - B. XtraDB.
    - C. InnoDB.
    - D. PostgreSQL.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: InnoDB is the only storage engine Amazon recommends for MySQL and MariaDB
    </details>

8. Which database engine supports the bring- your- own- license (BYOL) model? (Choose all that apply.)
    - A. Oracle Standard Edition Two.
    - B. Microsoft SQL Server.
    - C. Oracle Standard Edition One.
    - D. PostgreSQL.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: All editions of the Oracle database engine support the bring- your- own- license model in
    </details>

9. Which database instance class provides dedicated bandwidth for storage volumes?
    - A. Standard.
    - B. Memory optimized.
    - C. Storage optimized.
    - D. Burstable performance.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Memory- optimized instances are EBS optimized, providing dedicated bandwidth for
    </details>

10. If a MariaDB database running in RDS needs to write 200 MB of data every second, how many IOPS should you provision using io1 storage to sustain this performance?
    - A. 12,800.
    - B. 25,600.
    - C. 200.
    - D. 16.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: MariaDB has a page size of 16 KB. To write 200 MB (204,800 KB) of data every second,
    </details>

11. Using general- purpose SSD storage, how much storage would you need to allocate to get 600 IOPS?
    - A. 200 GB.
    - B. 100 GB.
    - C. 200 TB.
    - D. 200 MB.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: General- purpose SSD storage allocates three IOPS per gigabyte, up to 10,000
    </details>

12. If you need to achieve 12,000 IOPS using provisioned IOPS SSD storage, how much storage should you allocate, assuming that you need only 100 GB of storage?
    - A. There is no minimum storage requirement.
    - B. 200 GB.
    - C. 240 GB.
    - D. 12 TB.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: When you provision IOPS using io1 storage, you must do so in a ratio no greater than
    </details>

13. What type of database instance only accepts queries?
    - A. Read replica.
    - B. Standby database instance.
    - C. Primary database instance.
    - D. Master database instance.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: A read replica only services queries and cannot write to a database. A standby database
    </details>

14. In a multi- AZ deployment using Oracle, how is data replicated?
    - A. Synchronously from the primary instance to a read replica.
    - B. Synchronously using a cluster volume.
    - C. Asynchronously from the primary to a standby instance.
    - D. Synchronously from the primary to a standby instance.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Multi- AZ deployments using Oracle, PostgreSQL, MariaDB, MySQL, or Microsoft SQL
    </details>

15. Which of the following occurs when you restore a failed database instance from a snapshot?
    - A. RDS restores the snapshot to a new instance.
    - B. RDS restores the snapshot to the failed instance.
    - C. RDS restores only the individual databases to a new instance.
    - D. RDS deletes the snapshot.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: When you restore from a snapshot, RDS creates a new instance and doesn’t make any
    </details>

16. Which Redshift distribution style stores all tables on all compute nodes?
    - A. EVEN.
    - B. ALL.
    - C. KEY.
    - D. ODD.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The ALL distribution style ensures every compute node has a complete copy of every
    </details>

17. Which Redshift node type can store up to 326 TB of data?
    - A. Dense memory.
    - B. Leader.
    - C. Dense storage.
    - D. Dense compute.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The dense compute type can store up to 326 TB of data on magnetic storage. The dense
    </details>

18. Which is true regarding a primary key in a nonrelational database? (Choose all that apply.)
    - A. It’s required to uniquely identify an item.
    - B. It must be unique within the table.
    - C. It’s used to correlate data across different tables.
    - D. Its data type can vary within a table.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B
      Explanation: In a nonrelational database, a primary key is required to uniquely identify an item and
    </details>

19. In a DynamoDB table containing orders, which key would be most appropriate for storing an order date?
    - A. Partition key.
    - B. Sort key.
    - C. Hash key.
    - D. Simple primary key.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: An order date would not be unique within a table, so it would be inappropriate for
    </details>

20. When creating a DynamoDB table, how many read capacity units should you provision to be able to sustain strongly consistent reads of 11 KB per second?
    - A. 3.
    - B. 2.
    - C. 1.
    - D. 0.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: A single strongly consistent read of an item up to 4 KB consumes one read capacity unit.
    </details>

21. Which Redshift node type can provide the fastest read access?
    - A. Dense compute.
    - B. Dense storage.
    - C. Leader.
    - D. KEY.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The dense storage node type uses fast SSDs, whereas the dense compute node uses slower
    </details>

22. Which DynamoDB index type allows the partition and hash key to differ from the base table?
    - A. Eventually consistent index.
    - B. Local secondary index.
    - C. Global primary index.
    - D. Global secondary index.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: When you create a table, you can choose to create a global secondary index with a differ-
    </details>

23. To ensure the best performance, in which of the following situations would you choose to store data in a NoSQL database instead of a relational database?
    - A. You need to perform a variety of complex queries against the data.
    - B. You need to query data based on only one attribute.
    - C. You need to store JSON documents.
    - D. The data will be used by different applications.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: NoSQL databases are optimized for queries against a primary key. If you need to query
    </details>

24. What type of database can discover how different items are related to each other?
    - A. SQL.
    - B. Relational.
    - C. Document- oriented store.
    - D. Graph.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: A graph database is a type of nonrelational database that discovers relationships among
    </details>
