# Solutions Architect Ch12: Secure Architectures

1. Which of the following options can you not set in a password policy? (Choose two.)
    - A. Maximum length.
    - B. Require the use of numbers.
    - C. Prevent multiple users from using the same password.
    - D. Require an administrator to reset an expired password.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: A password policy can specify a minimum password length but not a maximum. It
    </details>

2. An IAM user is attached to a customer- managed policy granting them sufficient access to carry out their duties. You want to require multifactor authentication (MFA) for this user to use the AWS CLI. What element should you change in the policy?
    - A. Resource.
    - B. Condition.
    - C. Action.
    - D. Principal.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The Condition element lets you require MFA to grant the permissions defined in the
    </details>

3. You created an IAM policy that another administrator subsequently modified. You need to restore the policy to its original state but don’t remember how it was configured. What should you do to restore the policy? (Choose two.)
    - A. Consult CloudTrail global management event logs.
    - B. Restore the policy from a snapshot.
    - C. Consult CloudTrail data event logs.
    - D. Revert to the previous policy version.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: IAM keeps five versions of every customer- managed policy. When CloudTrail is config-
    </details>

4. An IAM user with full access to all EC2 actions in all regions assumes a role that has access to only the EC2 RunInstances operation in the us- east- 1 region. What will the user be able to do under the assumed role?
    - A. Create a new instance in any region.
    - B. Create a new instance in the us- east- 1 region.
    - C. Start an existing instance in the us- east- 1 region.
    - D. Start an existing instance in any region.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: When an IAM user assumes a role, the user gains the permissions assigned to that role but
    </details>

5. Several objects in a S3 bucket are encrypted using a KMS customer master key. Which of the following will give an IAM user permission to decrypt these objects?
    - A. Add the user to the key policy as a key user.
    - B. Grant the user access to the key using an IAM policy.
    - C. Add the user to the key policy as a key administrator.
    - D. Add the user as a principal to the bucket policy.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Granting a user access to use a KMS key to decrypt data requires adding the user to the
    </details>

6. You’re running a web server that keeps a detailed log of web requests. You want to determine which IP address has made the most requests in the last 24 hours. What should you do to accomplish this? (Choose two.)
    - A. Create a metric filter.
    - B. Stream the web server logs to CloudWatch Logs.
    - C. Upload the web server log to S3.
    - D. Use Athena to query the data.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: Athena lets you perform advanced SQL queries against data stored in S3. A metric
    </details>

7. An application running on an EC2 instance has been updated to send large amounts of data to a server in your datacenter for backup. Previously, the instance generated very little traffic. Which GuardDuty finding type is this likely to trigger?
    - A. Behavior.
    - B. Backdoor.
    - C. Stealth.
    - D. ResourceConsumption.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The Behavior finding type is triggered by an instance sending abnormally large amounts
    </details>

8. You’ve set up an AWS Config managed rule to check whether a particular security group is attached to every instance in a VPC. You receive an SNS notification that an instance is out of compliance. But when you check the instance a few hours later, the security group is attached. Which of the following may help explain the apparent discrepancy? (Choose two.)
    - A. The AWS Config timeline.
    - B. Lambda logs.
    - C. CloudTrail management event logs.
    - D. VPC flow logs.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: The AWS Config timeline will show every configuration change that occurred on
    </details>

9. You want to use Amazon Inspector to analyze the security posture of your EC2 instances running Windows. Which rules package should you not use in your assessment?
    - A. Common Vulnerabilities and Exposures.
    - B. Center for Internet Security Benchmarks.
    - C. Runtime Behavior Analysis.
    - D. Security Best Practices.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The Security Best Practices rules package has rules that apply to only Linux instances. The
    </details>

10. You have a distributed application running in datacenters around the world. The applica- tion connects to a public Simple Queue Service (SQS) endpoint to send messages to a queue. How can you prevent an attacker from using this endpoint to gain unauthorized access to the queue? (Choose two.)
    - A. Network access control lists.
    - B. Security groups.
    - C. IAM policies.
    - D. SQS access policies.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: You can use an IAM policy or SQS access policy to restrict queue access to certain
    </details>

11. You’re using a public- facing application load balancer to forward traffic to EC2 instances in an Auto Scaling group. What can you do to ensure users on the Internet can reach the load balancer over HTTPS without reaching your instances directly? (Choose two.)
    - A. Create a security group that allows all inbound traffic to TCP port 443.
    - B. Attach the security group to the instances.
    - C. Attach the security group to the load balancer.
    - D. Remove the Internet gateway from the VPC.
    - E. Create a security group that allows all inbound traffic to TCP port 80.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: HTTPS traffic traverses TCP port 443, so the security group should allow inbound
    </details>

12. You’re running a UDP- based application on an EC2 instance. How can you protect it against a DDoS attack?
    - A. Place the instance behind a network load balancer.
    - B. Implement a security group to restrict inbound access to the instance.
    - C. Place the instance behind an application load balancer.
    - D. Enable AWS Shield Standard.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: A security group to restrict inbound access to authorized sources is sufficient to guard
    </details>

13. You’re running a web application on six EC2 instances behind a network load balancer. The web application uses a MySQL database. How can you protect your application against SQL injection attacks? (Choose two.)
    - A. Enable WAF.
    - B. Assign elastic IP addresses to the instances.
    - C. Place the instances behind an application load balancer.
    - D. Block TCP port 3306.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: WAF can block SQL injection attacks against your application, but only if it’s behind
    </details>

14. Which services protect against an HTTP flood attack?
    - A. GuardDuty.
    - B. WAF.
    - C. Shield Standard.
    - D. Shield Advanced.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: Both WAF and Shield Advanced can protect against HTTP flood attacks, which are
    </details>
