# Solutions Architect Ch1: Introduction to Cloud Computing and AWS

1. Your developers want to run fully provisioned EC2 instances to support their application code deployments but prefer not to have to worry about manually configuring and launching the necessary infrastructure. Which of the following should they use?
    - A. AWS Lambda.
    - B. AWS Elastic Beanstalk.
    - C. Amazon EC2 Auto Scaling.
    - D. Amazon Route 53.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Elastic Beanstalk takes care of the ongoing underlying deployment details for you, allow-
    </details>

2. Some of your application’s end users are complaining of delays when accessing your resources from remote geographic locations. Which of these services would be the most likely to help reduce the delays?
    - A. Amazon CloudFront.
    - B. Amazon Route 53.
    - C. Elastic Load Balancing.
    - D. Amazon Glacier.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: CloudFront maintains a network of endpoints where cached versions of your application
    </details>

3. Which of the following is the best use- case scenario for Elastic Block Store?
    - A. You need a cheap and reliable place to store files your application can access.
    - B. You need a safe place to store backup archives from your local servers.
    - C. You need a source for on- demand compute cycles to meet fluctuating demand for your.
    - D. You need persistent storage for the filesystem run by your EC2 instance.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Elastic Block Store provides virtual block devices (think: storage drives) on which you can
    </details>

4. You need to integrate your company’s local user access controls with some of your AWS resources. Which of the following can help you control the way your local users access your AWS services and administration console? (Choose two.)
    - A. AWS Identity and Access Management (IAM).
    - B. Key Management Service (KMS).
    - C. AWS Directory Service.
    - D. Simple WorkFlow (SWF).
    - E. Amazon Cognito.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: AWS IAM lets you create user accounts, groups, and roles and assign them rights and
    </details>

5. The data consumed by the application you’re planning will require more speed and flexibility than you can get from a closely defined relational database structure. Which AWS database service should you choose?
    - A. Relational Database Service (RDS).
    - B. Amazon Aurora.
    - C. Amazon DynamoDB.
    - D. Key Management Service (KMS).

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: DynamoDB provides a NoSQL (nonrelational) database service. Both are good for work-
    </details>

6. You’ve launched an EC2 application server instance in the AWS Ireland region and you need to access it from the web. Which of the following is the correct endpoint address that you should use?
    - A. compute.eu- central- 1.amazonaws.com.
    - B. ec2.eu- central- 1.amazonaws.com.
    - C. elasticcomputecloud.eu- west- 2.amazonaws.com.
    - D. ec2.eu- west- 1.amazonaws.com.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: EC2 endpoints will always start with an ec2 prefix followed by the region designation
    </details>

7. When working to set up your first AWS deployment, you keep coming across the term avail- ability zone. What exactly is an availability zone?
    - A. An isolated physical datacenter within an AWS region.
    - B. A region containing multiple isolated datacenters.
    - C. A single network subnet used by resources within a single region.
    - D. A single isolated server room within a datacenter.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: An availability zone is an isolated physical datacenter within an AWS region. Regions are
    </details>

8. As you plan your multi- tiered, multi- instance AWS application, you need a way to effectively organize your instances and configure their network connectivity and access control. Which tool will let you do that?
    - A. Load Balancing.
    - B. Amazon Virtual Private Cloud (VPC).
    - C. Amazon CloudFront.
    - D. AWS endpoints.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: VPCs are virtualized network environments where you can control the connectivity of
    </details>

9. You want to be sure that the application you’re building using EC2 and S3 resources will be reliable enough to meet the regulatory standards required within your industry. What should you check?
    - A. Historical uptime log records.
    - B. The AWS Program Compliance Tool.
    - C. The AWS service level agreement (SLA).
    - D. The AWS Compliance Programs documentation page.
    - E. The AWS Shared Responsibility Model.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: The AWS service level agreement tells you the level of service availability you can realisti-
    </details>
