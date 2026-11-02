# Solutions Architect Ch3: AWS Storage

1. Your organization runs Linux- based EC2 instances that all require low- latency read/write access to a single set of files. Which of the following AWS services are your best choices? (Choose two.)
    - A. AWS Storage Gateway.
    - B. AWS S3.
    - C. Amazon Elastic File System.
    - D. AWS Elastic Block Store.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: Storage Gateway and EFS provide the required read/write access. S3 can be used to
    </details>

2. Your organization expects to be storing and processing large volumes of data in many small increments. When considering S3 usability, you’ll need to know whether you’ll face any prac- tical limitations in the use of AWS account resources. Which of the following will normally be available only in limited amounts?
    - A. PUT requests/month against an S3 bucket.
    - B. The volume of data space available per S3 bucket.
    - C. Account- wide S3 storage space.
    - D. The number of S3 buckets within a single account.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: In theory, at least, there’s no limit to the data you can upload to a single bucket or to all
    </details>

3. You have a publicly available file called filename stored in an S3 bucket named bucketname. Which of the following addresses will successfully retrieve the file using a web browser?
    - A. s3.amazonaws.com/bucketname/filename.
    - B. filename/bucketname.s3.amazonaws.com.
    - C. s3://bucketname/filename.
    - D. s3://filename/bucketname.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: HTTP (web) requests must address the s3.amazonaws.com domain along with the
    </details>

4. If you want the files stored in an S3 bucket to be accessible using a familiar directory hier- archy system, you’ll need to specify prefixes and delimiters. What are prefixes and delimiters?
    - A. A prefix is the name common to the objects you want to group, and a delimiter is the.
    - B. A prefix is the DNS name that precedes the amazonaws.com domain, and a delimiter is.
    - C. A prefix is the name common to the objects you want to group, and a delimiter is a.
    - D. A prefix is the name common to the file type you want to identify, and a delimiter is a.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: A prefix is the name common to the objects you want to group, and a slash character (/)
    </details>

5. Your web application relies on data objects stored in AWS S3 buckets. Compliance with industry regulations requires that those objects be encrypted and that related events be closely tracked. Which combination of tools should you use? (Choose two.)
    - A. Server- side encryption.
    - B. Amazon S3- Managed Keys.
    - C. AWS KMS- Managed Keys.
    - D. Client- side encryption.
    - E. AWS End- to- End managed keys.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: Client- side encryption occurs before an object reaches the bucket (i.e., before it comes
    </details>

6. You are engaged in a deep audit of the use of your AWS resources and you need to better understand the structure and content of your S3 server access logs. Which of the following operational details are likely to be included in S3 server access logs? (Choose three.)
    - A. Source bucket name.
    - B. Action requested.
    - C. Current bucket size.
    - D. API bucket creation calls.
    - E. Response status.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, E
      Explanation: S3 server access logs don’t report the source bucket’s current size. They don’t track
    </details>

7. You’re assessing the level of durability you’ll need to sufficiently ensure the long- term viability of a new web application you’re planning. Which of the following risks are covered by S3’s data durability guarantees? (Choose two.)
    - A. User misconfiguration.
    - B. Account security breach.
    - C. Infrastructure failure.
    - D. Temporary service outages.
    - E. Datacenter security breach.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, E
      Explanation: The S3 guarantee only covers the physical infrastructure owned by AWS. Temporary
    </details>

8. Which of the following explains the difference in durability between S3’sStandard- IA and S3 Intelligent- Tiering classes?
    - A. Standard- IA data has only 99.9% availability, whereas Intelligent- Tiering’s availability.
    - B. Standard- IA data is heavily replicated but only within a single availability zone, whereas.
    - C. Standard- IA data is replicated across AWS regions, whereas Intelligent- Tiering data is.
    - D. Standard- IA data is automatically backed up to Amazon Glacier, whereas Intelligent-.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Standard- IA data has only a 99.9% availability rate, whereas the availability (and other
    </details>

9. Which of the following is the 12- month availability guarantee for the S3 Standard- IA class?
    - A. 99.99 percent.
    - B. 99.9 percent.
    - C. 99.999999999 percent.
    - D. 99.5 percent.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The S3 Standard- IA (Infrequent Access) class is guaranteed to be available 99.9 percent of
    </details>

10. Your application regularly writes data to an S3 bucket, but you’re worried about the poten- tial for data corruption as a result of conflicting concurrent operations. Which of the follow- ing data operations would not be subject to concerns about eventual consistency?
    - A. Operations immediately preceding the deletion of an existing object.
    - B. Operations subsequent to the updating of an existing object.
    - C. Operations subsequent to the deletion of an existing object.
    - D. Operations subsequent to the creation of a new object.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: S3 can’t guarantee instant consistency across their infrastructure for changes to existing
    </details>

11. You’re worried that updates to the important data you store in S3 might incorrectly over- write existing files. What must you do to protect objects in S3 buckets from being acciden- tally lost?
    - A. Nothing. S3 protects existing files by default.
    - B. Nothing. S3 saves older versions of your files by default.
    - C. Enable versioning.
    - D. Enable file overwrite protection.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Object versioning must be manually enabled for each object to prevent older versions of
    </details>

12. Your S3 buckets contain many thousands of objects. Some of them could be moved to less expensive storage classes and others still require instant availability. How can you apply transitions between storage classes for only certain objects within an S3 bucket?
    - A. By specifying particular prefixes when you define your life cycle rules.
    - B. This isn’t possible. Life cycle rules must apply to all the objects in a bucket.
    - C. By specifying particular prefixes when you create the bucket.
    - D. By importing a predefined life cycle rule template.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: S3 life cycle rules can incorporate specifying objects by prefix. There’s no such thing as a
    </details>

13. Which of the following classes will usually make the most sense for long- term storage when included within a sequence of life cycle rules?
    - A. S3 Glacier Flexible Retrieval.
    - B. Reduced Redundancy.
    - C. S3 One Zone- IA.
    - D. S3 Standard- IA.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: S3 Glacier offers the least expensive and most highly resilient storage within the AWS eco-
    </details>

14. Which of the following are the recommended methods for providing secure and controlled access to your buckets? (Choose two.)
    - A. S3 access control lists (ACLs).
    - B. S3 bucket policies.
    - C. IAM policies.
    - D. Security groups.
    - E. AWS Key Management Service.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: ACLs are a legacy feature that isn’t as flexible as IAM or S3 bucket polices. Security
    </details>
