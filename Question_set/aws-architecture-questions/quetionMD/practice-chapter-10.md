# Solutions Architect Ch10: Resilient Architectures

1. What’s the minimum level of availability you need to stay under 30 minutes of downtime per month?
    - A. 99 percent.
    - B. 99.9 percent.
    - C. 99.95 percent.
    - D. 99.999 percent.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Availability of 99.95 percent translates to about 22 minutes of downtime per month, or
    </details>

2. Your application runs on two EC2 instances in one availability zone. An elastic load balancer distributes user traffic evenly across the healthy instances. The application on each instance connects to a single RDS database instance. Assuming each EC2 instance has an availability of 90 percent and the RDS instance has an availability of 95 percent, what is the total appli- cation availability?
    - A. 94.05 percent.
    - B. 99 percent.
    - C. 99.9 percent.
    - D. 99.95 percent.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The EC2 instances are redundant components, so to calculate their availability, you mul-
    </details>

3. Your organization is designing a new application to run on AWS. The developers have asked you to recommend a database that will perform well in all regions. Which database should you recommend for maximum availability?
    - A. Multi- AZ RDS using MySQL.
    - B. DynamoDB.
    - C. Multi- AZ RDS using Aurora.
    - D. A self- hosted SQL database.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: DynamoDB offers 99.99 percent availability and low latency. Because it’s distributed,
    </details>

4. Which of the following can help you increase the availability of a web application? (Choose all that apply.)
    - A. Store web assets in an S3 bucket instead of on the application instance.
    - B. Use instance classes large enough to handle your application’s peak load.
    - C. Scale your instances in.
    - D. Scale your instances out.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: One cause of application failures is resource exhaustion. By scoping out large enough
    </details>

5. You’ve configured an EC2 Auto Scaling group to use a launch configuration to provision and install an application on several instances. You now need to reconfigure Auto Scaling to install an additional application on new instances. Which of the following should you do?
    - A. Modify the launch configuration.
    - B. Create a launch template and configure the Auto Scaling group to use it.
    - C. Modify the launch template.
    - D. Modify the CloudFormation template.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: You can modify a launch template by creating a new version of it; however, the question
    </details>

6. You create an Auto Scaling group with a minimum group size of 3, a maximum group size of 10, and a desired capacity of 5. You then manually terminate two instances in the group. Which of the following will Auto Scaling do?
    - A. Create two new instances.
    - B. Reduce the desired capacity to 3.
    - C. Nothing.
    - D. Increment the minimum group size to 5.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Auto Scaling strives to maintain the number of instances specified in the desired capacity
    </details>

7. Which of the following can Auto Scaling use for instance health checks? (Choose all that apply.)
    - A. ELB health checks.
    - B. CloudWatch Alarms.
    - C. Route 53 health checks.
    - D. EC2 system checks.
    - E. EC2 instance checks.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D, E
      Explanation: Auto Scaling monitors the health of instances in the group using either ELB or
    </details>

8. You’re running an application that receives a spike in traffic on the first day of every month. You want to configure Auto Scaling to add more instances before the spike begins and then add additional instances in proportion to the CPU utilization of each instance. Which of the following should you implement? (Choose all that apply.)
    - A. Target tracking policies.
    - B. Scheduled actions.
    - C. Step scaling policies.
    - D. Simple scaling policies.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: Scheduled actions can adjust the minimum and maximum group sizes and the desired
    </details>

9. Which of the following provide the most protection against data corruption and accidental deletion for existing objects stored in S3? (Choose two.)
    - A. Versioning.
    - B. Bucket policies.
    - C. Cross- region replication.
    - D. Using the Standard storage class.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Enabling versioning protects objects against data corruption and deletion by keeping
    </details>

10. You need to maintain three days of backups for binary files stored across several EC2 instances in a spot fleet. What’s the best way to achieve this?
    - A. Stream the files to CloudWatch Logs.
    - B. Create an Elastic File System and back up the files to it using a cron job.
    - C. Create a Snapshot Lifecycle Policy to snapshot each instance every 24 hours and retain.
    - D. Create a Snapshot Lifecycle Policy to snapshot each instance every 4 hours and retain.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: The Data Lifecycle Manager can automatically create snapshots of an EBS volume every
    </details>

11. You plan to run multi- AZ RDS across three availability zones in a region. You want to have two read replicas per zone. Which database engine should you choose?
    - A. MySQL.
    - B. PostgreSQL.
    - C. MySQL.
    - D. Aurora.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Aurora allows you to have up to 15 replicas. MariaDB, MySQL, and PostgreSQL allow
    </details>

12. You’re running an RDS instance in one availability zone. What should you implement to be able to achieve a recovery point objective (RPO) of five minutes?
    - A. Configure multi- AZ.
    - B. Enable automated snapshots.
    - C. Add a read replica in the same region.
    - D. Add a read replica in a different region.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: When you enable automated snapshots, RDS backs up database transaction logs about
    </details>

13. When creating subnets in a VPC, what are two reasons to leave sufficient space in the VPC for more subnets later? (Choose two.)
    - A. You may need to add another tier for your application.
    - B. You may need to implement RDS.
    - C. AWS occasionally adds more availability zones to a region.
    - D. You may need to add a secondary CIDR to the VPC.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: AWS sometimes adds additional availability zones to a region. To take advantage of a
    </details>

14. You plan to deploy 50 EC2 instances, each with two private IP addresses. To put all of these instances in a single subnet, which subnet CIDRs could you use? (Choose all that apply.)
    - A. 172.21.0.0/25.
    - B. 172.21.0.0/26.
    - C. 10.0.0.0/8.
    - D. 10.0.0.0/21.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Fifty EC2 instances, each with two private IP addresses, would consume 100 IP
    </details>

15. You’re currently connecting to your AWS resources using a 10 Gbps Internet connection at your office. You also have end users around the world who access the same AWS resources. What are two reasons you may consider using Direct Connect in addition to your Internet connection? (Choose two.)
    - A. Lower latency.
    - B. Higher bandwidth.
    - C. Better end- user experience.
    - D. Increased security.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Direct Connect offers consistent speeds and latency to the AWS cloud. Because Direct
    </details>

16. Before connecting a VPC to your datacenter, what must you do to ensure proper connectivity?
    - A. Use IAM policies to restrict access to AWS resources.
    - B. Ensure the IP address ranges in the networks don’t overlap.
    - C. Ensure security groups on your datacenter firewalls are properly configured.
    - D. Use in- transit encryption.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: When connecting a VPC to an external network, whether via a VPN connection or Direct
    </details>

17. You plan to run a stand- alone Linux application on AWS and need 99 percent availability. The application doesn’t require a database, and only a few users will access it. You will occasionally need to terminate and re- create the instance using a different AMI. Which of the following should you use? (Choose all that apply.)
    - A. CloudFormation.
    - B. Auto Scaling.
    - C. User data.
    - D. Dynamic scaling policies.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: CloudFormation lets you provision and configure EC2 instances by defining your
    </details>

18. You need eight instances running simultaneously in a single region. Assuming three availability zones are available, what’s the minimum number of instances you must run in each zone to be able to withstand a single zone failure?
    - A. 3.
    - B. 16.
    - C. 8.
    - D. 4.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: By running four instances in each zone, you have a total of 12 instances in the region.
    </details>

19. If your application is down for 45 minutes a year, what is its approximate availability?
    - A. 99 percent.
    - B. 99.9 percent.
    - C. 99.99 percent.
    - D. 99.95 percent.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Availability of 99.99 percent corresponds to about 52 minutes of downtime per year; 99
    </details>

20. You’re running an application in two regions and using multi- AZ RDS with read replicas in both regions. Users normally access the application in only one region by browsing to a public domain name that resolves to an elastic load balancer. If that region fails, which of the following should you do to fail over to the other region? (Choose all that apply.)
    - A. Update the DNS record to point to the load balancer in the other region.
    - B. Point the load balancer to the other region.
    - C. Fail over to the database in the other region.
    - D. Restore the database from a snapshot.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: Because users access a public domain name that resolves to an elastic load balancer,
    </details>

21. When a consumer grabs a message from an SQS queue, what happens to the message? (Choose two.)
    - A. It is immediately deleted from the queue.
    - B. It remains in the queue for 30 seconds and is then deleted.
    - C. It stays in the queue for the remaining duration of the retention period.
    - D. It becomes invisible to other consumers for the duration of the visibility timeout.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: After a consumer grabs a message, the message is not deleted. Instead, the message
    </details>

22. What is the default visibility timeout for an SQS queue?
    - A. 0 seconds.
    - B. 30 seconds.
    - C. 12 hours.
    - D. 7 days.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The default visibility timeout for a queue is 30 seconds. It can be configured to between 0
    </details>

23. What is the default retention period for an SQS queue?
    - A. 30 minutes.
    - B. 1 hour.
    - C. 1 day.
    - D. 4 days.
    - E. 7 days.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The default retention period is 4 days but can be set to between 1 minute and 14 days.
    </details>

24. You want to make sure that only specific messages placed in an SQS queue are not available for consumption for 10 minutes. Which of the following settings can you use to achieve this?
    - A. Delay queue.
    - B. Message timer.
    - C. Visibility timeout.
    - D. Long polling.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: You can use a message timer to hide a message for up to 15 minutes. Per- queue delay set-
    </details>

25. Which of the following SQS queue types can handle over 50,000 in- flight messages?
    - A. FIFO.
    - B. Standard.
    - C. Delay.
    - D. Short.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: A standard queue can handle up to 120,000 in- flight messages. A FIFO queue can handle
    </details>

26. What SQS queue type always delivers messages in the order they were received?
    - A. FIFO.
    - B. Standard.
    - C. LIFO.
    - D. FILO.
    - E. Basic.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: FIFO queues always deliver messages in the order they were received. Standard queues
    </details>

27. You have an application that uses long polling to retrieve messages from an SQS queue. Occasionally, the application crashes because of duplicate messages. Which of the following might resolve the issue?
    - A. Configure a per- queue delay.
    - B. Use a standard queue.
    - C. Use a FIFO queue.
    - D. Use short polling.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Standard queues may occasionally deliver a message more than once. FIFO queues will
    </details>

28. A producer application places messages in an SQS queue, and consumer applications poll the queue every 5 seconds using the default polling method. Occasionally, when a consumer polls the queue, SQS reports there are no messages in the queue, even though there are. When the consumer subsequently polls the queue, SQS delivers the messages. Which of the following may explain the missing messages?
    - A. Using long polling.
    - B. Using short polling.
    - C. Using a FIFO queue.
    - D. Using a standard queue.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Short polling, which is the default, may occasionally fail to deliver messages. To ensure
    </details>

29. Which of the following situations calls for a dead- letter queue?
    - A. A message sits in the queue for too long and gets deleted.
    - B. Different consumers receive and process the same message.
    - C. Messages are mysteriously disappearing from the queue.
    - D. A consumer repeatedly fails to process a particular message.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Dead- letter queues are for messages that a consumer is unable to process. To use
    </details>

30. A message that’s 6 days old is sent to a dead- letter queue. The retention period for the dead- letter queue and the source queue is 10 days. What will happen to the message?
    - A. It will sit in the dead- letter queue for up to 10 days.
    - B. It will be immediately deleted.
    - C. It will be deleted after four days.
    - D. It will sit in the dead- letter queue for up to 20 days.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: If the retention period for the dead- letter queue is 10 days, and a message is already
    </details>
