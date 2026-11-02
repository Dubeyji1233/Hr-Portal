# Solutions Architect Assessment Test

1. True/false: The Developer Support plan provides access to a support application program- ming interface (API).
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The Business plan offers access to a support API, but the Developer plan does not. See
    </details>

2. True/false: AWS is responsible for managing the network configuration of your EC2 instances.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Customers are responsible for managing the network configuration of EC2 instances.
    </details>

3. Which of the following services is most useful for decoupling the components of a monolithic application?
    - A. SNS.
    - B. KMS.
    - C. SQS.
    - D. Glacier.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Simple Queue Service (SQS) allows for event- driven messaging within distributed systems
    </details>

4. An application you want to run on EC2 requires you to license it based on the number of physical CPU sockets and cores on the hardware you plan to run the application on. Which of the following tenancy models should you specify?
    - A. Dedicated host.
    - B. Dedicated instance.
    - C. Shared tenancy.
    - D. Bring your own license.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The dedicated host option lets you see the number of physical CPU sockets and cores on a
    </details>

5. True/false: Changing the instance type of an EC2 instance will change its elastic IP address.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: An elastic IP address will not change. A public IP address attached to an instance will
    </details>

6. True/false: You can use a Quick Start Amazon Machine Image (AMI) to create any instance type.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: A Quick Start AMI is independent of the instance type. See Chapter 2 for more
    </details>

7. Which S3 encryption option does not require AWS persistently storing the encryption keys it uses to decrypt data?
    - A. Client- side encryption.
    - B. SSE- KMS.
    - C. SSE- S3.
    - D. SSE- C.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: With SSE- C you provide your own keys for Amazon to use to decrypt and encrypt your
    </details>

8. True/false: Durability measures the percentage of likelihood that a given object will not be inadvertently lost by AWS over the course of a year.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Durability corresponds to an average annual expected loss of objects stored on S3, not
    </details>

9. True/false: After uploading a new object to S3, there will be a slight delay (one to two seconds) before the object is available.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: S3 uses a read- after- write consistency model for new objects, so once you upload an
    </details>

10. You created a virtual private cloud (VPC) using the Classless Inter- Domain Routing (CIDR) block 10.0.0.0/24. You need to connect to this VPC from your internal network, but the IP addresses in use on your internal network overlap with the CIDR. Which of the following is a valid way to address this problem?
    - A. Remove the CIDR and use IPv6 instead.
    - B. Change the VPC’s CIDR.
    - C. Create a new VPC with a different CIDR.
    - D. Create a secondary CIDR for the VPC.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: You can’t change the primary CIDR for a VPC, so you must create a new one to connect
    </details>

11. True/false: An EC2 instance must be in a public subnet to access the Internet.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: An EC2 instance can access the Internet from a private subnet provided it uses a NAT
    </details>

12. True/false: The route table for a public subnet must have a default route pointing to an Internet gateway as a target.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The definition of a public subnet is a subnet that has a default route pointing to an Inter-
    </details>

13. Which of the following use cases is well suited for DynamoDB?
    - A. Running a MongoDB database on AWS.
    - B. Storing large binary files exceeding 1 GB in size.
    - C. Storing JSON documents that have a consistent structure.
    - D. Storing image assets for a website.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: DynamoDB is a key- value store that can be used to store items up to 400 KB in size. See
    </details>

14. True/false: You can create a DynamoDB global secondary index for an existing table at any time.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: You can create a global secondary index for an existing table at any time. You can create
    </details>

15. True/false: Enabling point- in- time RDS snapshots is sufficient to give you a recovery point objective (RPO) of less than 10 minutes.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Enabling point- in- time recovery gives you an RPO of about five minutes. The recovery
    </details>

16. Which of the following steps does the most to protect your AWS account?
    - A. Deleting unused Identity and Access Management (IAM) policies.
    - B. Revoking unnecessary access for IAM users.
    - C. Rotating root access keys.
    - D. Restricting access to S3 buckets.
    - E. Rotating Secure Shell (SSH) key pairs.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Revoking unnecessary access for IAM users is the most effective of the listed measures for
    </details>

17. Which of the following can be used to encrypt the operating system of an EC2 instance?
    - A. AWS Secrets Manager.
    - B. CloudHSM.
    - C. AWS Key Management Service (KMS).
    - D. AWS Security Token Service (STS).

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: KMS can be used to encrypt Elastic Block Store (EBS) volumes that store an instance’s
    </details>

18. What is a difference between a token generated by the AWS Security Token Service (STS) and an IAM access key?
    - A. The token generated by STS can’t be used by an IAM principal.
    - B. An IAM access key is unique.
    - C. The token generated by STS can be used only once.
    - D. The token generated by STS expires.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: STS tokens expire and IAM access keys do not. An STS token can be used more than
    </details>

19. True/false: EC2 sends instance memory utilization metrics to CloudWatch every five minutes.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: EC2 doesn’t track instance memory utilization. See Chapter 7 for more information.
    </details>

20. You configured a CloudWatch alarm to monitor CPU utilization for an EC2 instance. The alarm began in the INSUFFICIENT_DATA state and then entered the ALARM state. What can you conclude from this?
    - A. The instance recently rebooted.
    - B. CPU utilization is too high.
    - C. The CPU utilization metric crossed the alarm threshold.
    - D. The instance is stopped.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: The transition to the ALARM state simply implies that the metric crossed a
    </details>

21. Where do AWS Config and CloudTrail store their logs?
    - A. S3 buckets.
    - B. CloudWatch Logs.
    - C. CloudTrail Events.
    - D. DynamoDB.
    - E. Amazon Athena.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Both store their logs in S3 buckets. See Chapter 7 for more information.
    </details>

22. True/false: An EC2 instance in a private subnet can resolve an “A” resource record for a public hosted zone hosted in Route 53.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: An EC2 instance in a private subnet still has access to Amazon’s private DNS servers,
    </details>

23. You want to use Route 53 to send users to the application load balancer closest to them. Which of the following routing policies lets you do this with the least effort?
    - A. Latency routing.
    - B. Geolocation routing.
    - C. Geoproximity routing.
    - D. Edge routing.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Geoproximity routing routes users to the location closest to them. Geolocation routing
    </details>

24. True/false: You can use an existing domain name with Route 53 without switching its regis- tration to AWS.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Route 53 is a true DNS service in that it can host zones for any domain name. You can
    </details>

25. You’re designing an application that takes multiple image files and combines them into a video file that users on the Internet can download. Which of the following can help you quickly implement your application in the fastest, most highly available, and most cost- effective manner?
    - A. EC2 spot fleet.
    - B. Lambda.
    - C. Relational Database Service (RDS).
    - D. Auto Scaling.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Lambda is a highly available, reliable, “serverless” compute platform that runs functions
    </details>

26. You’re using EC2 Auto Scaling and want to implement a scaling policy that adds one extra instance only when the average CPU utilization of each instance exceeds 90 percent. However, you don’t want it to add more than one instance every five minutes. Which of the following scaling policies should you use?
    - A. Simple.
    - B. Step.
    - C. Target tracking.
    - D. PercentChangeInCapacity.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: A simple scaling policy changes the group size and then has a cooldown period before
    </details>

27. True/false: EC2 Auto Scaling automatically replaces group instances directly terminated by the root user.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Auto Scaling always attempts to maintain the minimum group size or, if set, the desired
    </details>

28. Which ElastiCache engine can persistently store data?
    - A. MySQL.
    - B. Memcached.
    - C. MongoDB.
    - D. Redis.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: ElastiCache supports Memcached and Redis, but only the latter can store data
    </details>

29. Which of the following is not an AWS service?
    - A. CloudFormation.
    - B. Puppet.
    - C. OpsWorks.
    - D. Snowball.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Puppet is a configuration management platform that AWS offers via OpsWorks but is not
    </details>

30. True/false: S3 cross- region replication uses transfer acceleration.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: S3 cross- region replication transfers objects between different buckets. Transfer
    </details>

31. Which of the following services can you deactivate on your account?
    - A. Security Token Service (STS).
    - B. CloudWatch.
    - C. Virtual private cloud (VPC).
    - D. Lambda.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: You can deactivate STS for all regions except US East. See Chapter 12 for more
    </details>

32. Which of the following services can alert you to malware on an EC2 instance?
    - A. AWS GuardDuty.
    - B. AWS Inspector.
    - C. AWS Shield.
    - D. AWS Web Application Firewall.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: GuardDuty looks for potentially malicious activity. Inspector looks for vulnerabilities that
    </details>

33. True/false: If versioning is enabled on an S3 bucket, applying encryption to an unencrypted object in that bucket will create a new, encrypted version of that object.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Applying encryption to an unencrypted object will create a new, encrypted version of that
    </details>

34. Which instance type will, if left running, continue to incur costs?
    - A. Spot.
    - B. Standard reserved.
    - C. On- demand.
    - D. Convertible reserved.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: On- demand instances will continue to run and incur costs. Reserved instances cost the
    </details>

35. True/false: The EBS Lifecycle Manager can take snapshots of volumes that were once attached to terminated instances.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The EBS Lifecycle Manager can take scheduled snapshots of any EBS volume, regardless
    </details>

36. Which of the following lets you spin up new web servers the quickest?
    - A. Lambda.
    - B. Auto Scaling.
    - C. Elastic Container Service.
    - D. CloudFront.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Elastic Container Service lets you run containers that can launch in a matter of seconds.
    </details>

37. True/false: CloudFormation stack names are case- sensitive.
    - A. True.
    - B. False.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Almost everything in CloudFormation is case sensitive. See Chapter 11 for more
    </details>
