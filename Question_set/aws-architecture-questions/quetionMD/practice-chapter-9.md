# Solutions Architect Ch9: Data Ingestion and Analytics

1. What are valid use cases for transforming data when importing it into a data lake? (Select three.)
    - A. Imposing consistent timestamps.
    - B. Removing corrupted data.
    - C. Creating a schema.
    - D. Removing duplicate data.
    - E. Visualizing data.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, D
      Explanation: Data transformation includes changing the contents or format of data. Creating a
    </details>

2. What AWS Data Lake transform detects duplicate data?
    - A. MatchFinder.
    - B. FindMatches ML.
    - C. Elastic MapReduce.
    - D. Spark.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: FindMatches ML is the name of the transform that detects duplicate data. MatchFinder
    </details>

3. What’s the most efficient way to import data from an on- premises SQL database into an AWS Data Lake?
    - A. Dump the database into an S3 bucket and then import the data into the data lake.
    - B. Import the data into RDS and then into the data lake.
    - C. Use the Glue Connector.
    - D. Use the JDBC connector.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Connecting to the SQL database using the JDBC connector and importing the data
    </details>

4. What protocols does AWS Transfer Family support? (Choose two.)
    - A. SFTP.
    - B. SMB.
    - C. FTP.
    - D. CIFS.
    - E. HTTPS.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: AWS Transfer Family supports SFTP, FTPS, and FTP. It doesn’t support CIFS/SMB or
    </details>

5. AWS Transfer Family can be used to transfer files to or from which of the following? (Choose two.)
    - A. EBS.
    - B. EFS.
    - C. RDP.
    - D. S3.
    - E. DynamoDB.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: AWS Transfer Family can transfer files to or from EFS or S3. It doesn’t support trans-
    </details>

6. What technology does AWS Glue use to search large data sets and perform data transformation?
    - A. Amazon Athena.
    - B. Apache Spark.
    - C. Apache Elephant Stack.
    - D. AWS Data Lake.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: AWS Glue uses the Apache Spark big data framework to perform search and transforms.
    </details>

7. What is the difference between a data lake and a data warehouse? (Choose two.)
    - A. A data warehouse can store unstructured data.
    - B. A data warehouse is a relational database.
    - C. A data lake requires structured data.
    - D. A data lake can store unstructured, schema- less data.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: A data warehouse is a relational OLAP database. A data lake can store both structured
    </details>

8. Which of the following can AWS Data Lake import from? (Choose two.)
    - A. EBS.
    - B. ELB.
    - C. CloudFront.
    - D. IAM.
    - E. CloudWatch.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: AWS Data Lake can import data from ELB and CloudFront, but none of the others.
    </details>

9. Which of the following can analyze data in an AWS Data Lake? (Choose two.)
    - A. Amazon EMS.
    - B. Athena.
    - C. RedShift Spectrum.
    - D. RedShift.
    - E. S3.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: Athena and RedShift Spectrum can analyze data in an AWS Data Lake. RedShift and
    </details>

10. Which of the following is not an appropriate use of AWS Glue?
    - A. Searching data.
    - B. Ingesting real- time streaming data.
    - C. Preparing data for analysis.
    - D. Transforming data.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Kinesis is more appropriate for real- time streaming data. For all other cases, AWS Glue is
    </details>
