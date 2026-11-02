# Solutions Architect Ch11: High-Performing Architectures

1. Which of the following are parameters used to describe the performance of specific EC2 instance types? (Choose three.)
    - A. ECUs (EC2 compute units).
    - B. vCPUs (virtual CPUs).
    - C. ACCpR (Aggregate Cumulative Cost per Request).
    - D. Intel AES- NI.
    - E. Maximum read replicas.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, D
      Explanation: ECUs, vCPUs, and the Intel AES- NI encryption set are all instance type parameters.
    </details>

2. As the popularity of your EC2- based application grows, you need to improve your infrastruc- ture so that it can better handle fluctuations in demand. Which of the following are normally necessary components for successful Auto Scaling? (Choose three.)
    - A. Launch configuration.
    - B. Load balancer.
    - C. Custom- defined EC2 AMI.
    - D. A start.sh script.
    - E. An AWS OpsWorks stack.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, C
      Explanation: A launch configuration pointing to an EC2 AMI and an associated load balancer are
    </details>

3. Which of the following best describes the role that launch configurations play in Auto Scaling?
    - A. Define the capacity metric that will trigger a scaling change.
    - B. Define the AMI to be deployed by Auto Scaling operations.
    - C. Control the minimum and maximum number of instances to allow.
    - D. Define the associated load balancer.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Defining a capacity metric, minimum and maximum instances, and a load balancer
    </details>

4. You’re considering building your new e- commerce application using a microservices architecture where individual servers are tasked with separate but complementary tasks (doc- ument server, database, cache, etc.). Which of the following is probably the best platform?
    - A. Elastic Container Service.
    - B. Lambda.
    - C. ECR.
    - D. Elastic Beanstalk.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Elastic Container Service is a good platform for microservices. Lambda functions execu-
    </details>

5. Your EC2 deployment profile would benefit from a traditional RAID configuration for the EBS volumes you’re using. Where are RAID- optimized EBS volume configurations performed?
    - A. From the EBS dashboard.
    - B. From the EC2 Storage Optimization dashboard.
    - C. From the AWS CLI.
    - D. From within the EC2 instance OS.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: RAID optimization is an OS- level configuration and can, therefore, be performed only
    </details>

6. Which of the following tools will provide both low- latency access and resilience for your S3- based data?
    - A. CloudFront.
    - B. RAID arrays.
    - C. Cross- region replication.
    - D. Transfer Acceleration.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Cross- region replication can provide both low- latency and resilience. CloudFront and S3
    </details>

7. Which of the following tools uses CloudFront edge locations to speed up data transfers?
    - A. Amazon S3 Transfer Acceleration.
    - B. S3 Cross- Region Replication.
    - C. EBS Data Transfer Wizard.
    - D. EC2 Auto Scaling.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: S3 Transfer Acceleration makes use of CloudFront locations. Neither S3 Cross- Region
    </details>

8. Your multi- tiered application has been experiencing slower than normal data reads and writes. As you work on improving performance, which of the following is not a major design consideration for a managed RDS database?
    - A. Optimizing indexes.
    - B. Optimizing scalability.
    - C. Optimizing schemas.
    - D. Optimizing views.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Scalability is managed automatically by RDS, and there is no way for you to improve it
    </details>

9. Which of the following are possible advantages of hosting a relational database on an EC2 instance over using the RDS service? (Choose two.)
    - A. Automated software patches.
    - B. Automated OS updates.
    - C. Out- of- the- box Auto Scaling.
    - D. Cost savings.
    - E. Greater host control.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D, E
      Explanation: Automated patches, out- of- the- box Auto Scaling, and updates are benefits of a
    </details>

10. You’ve received complaints from users that performance on your EC2- based graphics processing application is slower than normal. Demand has been rising over the past month or two, which could be a factor. Which of the following is the most likely to help? (Choose two.)
    - A. Moving your application to Amazon LightSail.
    - B. Switching to an EC2 instance that supports enhanced graphics.
    - C. Deploying Amazon Elasticsearch in front of your instance.
    - D. Increasing the instance limit on your Auto Scaling group.
    - E. Putting your application behind a CloudFront distribution.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: Integrated enhanced graphics and Auto Scaling can both help here. Amazon LightSail
    </details>

11. Which of the following load balancer types is optimized for TCP- based applications and preserves the source IP address?
    - A. Application load balancer.
    - B. Classic load balancer.
    - C. Network load balancer.
    - D. Gateway load balancer.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: The network load balancer is designed for any TCP- based application and preserves
    </details>

12. Which of the following can be used to configure a CloudFormation template? (Choose three.)
    - A. The CloudFormation drag- and- drop interface.
    - B. Selecting a prebuilt sample template.
    - C. Importing a template from AWS CloudDeploy.
    - D. Creating your own JSON template document.
    - E. Importing a template from Systems Manager.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, D
      Explanation: The CloudFormation wizard, prebuilt templates, and JSON formatting are all useful
    </details>

13. Which of the following details is not a necessary component of a CloudFormation configuration?
    - A. Default node name.
    - B. Stack name.
    - C. Database name.
    - D. DB User name.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: There is no default node name in a CloudFormation configuration- nor is there a node of
    </details>

14. Which of the following can be integrated into your AWS workflow through AWS OpsWorks? (Choose two.)
    - A. Ansible.
    - B. Chef.
    - C. Terraform.
    - D. SaltStack.
    - E. Puppet.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, E
      Explanation: Chef and Puppet are both integrated with AWS OpsWorks. Terraform, SaltStack, and
    </details>

15. Which of the following are important elements of a successful resource monitoring protocol? (Choose two.)
    - A. CloudWatch dashboards.
    - B. CloudWatch OneView.
    - C. SNS alerts.
    - D. AWS Config dashboards.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: Dashboards and SNS are important elements of resource monitoring. There are no
    </details>

16. Which of the following will most enhance the value of the CloudWatch data your resources generate? (Choose two.)
    - A. Predefined performance baselines.
    - B. Predefined key performance indicators (KPIs).
    - C. Advance permission from AWS.
    - D. A complete record of your account’s resource configuration changes.
    - E. A running Service Catalog task.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B
      Explanation: Advance permission from AWS is helpful only for penetration testing operations. A
    </details>

17. Which of the following can be used to audit the changes made to your account and resource configurations?
    - A. AWS CloudTrail.
    - B. AWS CloudWatch.
    - C. AWS CodePipeline.
    - D. AWS Config.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Config is an auditing tool. CloudTrail tracks API calls. CloudWatch monitors system
    </details>

18. Which of the following caching engines can be integrated with Amazon ElastiCache? (Choose two.)
    - A. Varnish.
    - B. Redis.
    - C. Memcached.
    - D. Nginx.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: ElastiCache executions can use either Redis or Memcached. Varnish and Nginx are
    </details>

19. Which of the following use case scenarios are a good fit for caching using Redis and ElastiCache? (Choose two.)
    - A. Your online application requires users’ session states to be saved and the behavior of all.
    - B. Your online application needs the fastest operation available.
    - C. Your admin is not familiar with caching and is looking for a relatively simple setup for a.
    - D. You’re not sure what your application needs might be in a month or two, so you want to.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Redis is useful for operations that require persistent session states and or greater flex-
    </details>

20. Which of the following database engines is not a candidate for read replicas within Amazon RDS?
    - A. MySQL.
    - B. DynamoDB.
    - C. MariaDB.
    - D. PostgreSQL.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: DynamoDB is not available at all in RDS, and certainly not as a read replica.
    </details>

21. When using CloudFormation to provision multiple stacks of related resources, by which of the following should you organize your resources into different stacks? (Choose two.)
    - A. Cost.
    - B. S3 bucket.
    - C. Life cycle.
    - D. Ownership.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: It’s a best practice to organize stacks by life cycle (e.g., development, test, production)
    </details>

22. Which of the following resource properties are good candidates for definition as parameters in a CloudFormation template? (Choose two.)
    - A. AMI ID.
    - B. EC2 key pair name.
    - C. Stack name.
    - D. Logical ID.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B
      Explanation: Parameters let you input custom values into a template when you create a stack. The
    </details>
