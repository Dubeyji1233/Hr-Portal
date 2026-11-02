# Solutions Architect Ch13: Cost-Optimized Architectures

1. Which of the following best describes the AWS Free Tier?
    - A. Free access to AWS services for a new account’s first month.
    - B. Free access to all instance types of AWS EC2 instances for new accounts.
    - C. Free access to basic levels of AWS services for a new account’s first year.
    - D. Unlimited and open- ended access to the “free tier” of most AWS services.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: The Free Tier provides free access to basic levels of AWS services for a new account’s
    </details>

2. Which of the following storage classes provides the least expensive storage and transfer rates?
    - A. Amazon S3 Glacier.
    - B. Amazon S3 Standard- Infrequent Access.
    - C. Amazon S3 Standard.
    - D. Amazon S3 One Zone- Infrequent Access.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Standard provides the most replicated and quickest- access service and is, therefore, the
    </details>

3. Which AWS service is best suited to controlling your spending by sending email alerts?
    - A. Cost Explorer.
    - B. Budgets.
    - C. Organizations.
    - D. TCO Calculator.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Cost Explorer provides usage and spending data. Organizations lets you combine multiple
    </details>

4. Your AWS infrastructure is growing and you’re beginning to have trouble keeping track of what you’re spending. Which AWS service is best suited to analyzing account usage data at scale?
    - A. Trusted Advisor.
    - B. Cost Explorer.
    - C. Budgets.
    - D. Cost and Usage Reports.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Cost Explorer provides usage and spending data, but without the ability to easily incor-
    </details>

5. Your company wants to more closely coordinate the administration of its multiple AWS accounts, and AWS Organizations can help it do that. How does that change your security profile? (Choose three.)
    - A. An organization- level administration account breach is potentially more damaging.
    - B. User permissions can be controlled centrally at the organization level.
    - C. You should upgrade to use only specially hardened organization- level VPCs.
    - D. Standard security best practices such as MFA and strong passwords are even more.
    - E. You should upgrade all of your existing security groups to account for the changes.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, D
      Explanation: As efficient as Organizations can be, so does the threat they represent grow. There is
    </details>

6. Which of the following resource states are monitored by AWS Trusted Advisor? (Choose two.)
    - A. Route 53 routing failures.
    - B. Running but idle EC2 instances.
    - C. S3 buckets with public read access permissions.
    - D. EC2 Linux instances that allow root account SSH access.
    - E. Unencrypted S3 bucket data transfers.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: Trusted Advisor monitors your EC2 instances for lower than 10 percent CPU and
    </details>

7. You’re planning a new AWS deployment, and your team is debating whether they’ll be better off using an RDS database or one run on an EC2 instance. Which of the following tools will be most helpful?
    - A. TCO Calculator.
    - B. AWS Pricing Calculator.
    - C. Trusted Advisor.
    - D. Cost and Usage Reports.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The Pricing Calculator is the most direct tool for this kind of calculation. TCO Calculator
    </details>

8. Which of the following is not a metric you can configure an AWS budget to track?
    - A. EBS volume capacity.
    - B. Resource usage.
    - C. Reserve instance coverage.
    - D. Resource cost.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Monitoring of EBS volumes for capacity is not within the scope of budgets.
    </details>

9. Which of the following statements are true of cost allocation tags? (Choose two.)
    - A. Tags can take up to 24 hours before they appear in the Billing and Cost Management.
    - B. Tags can’t be applied to resources that were launched before the tags were created.
    - C. You’re allowed five free budgets per account.
    - D. You can activate and manage cost allocation tags from the Tag Editor page.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B
      Explanation: Tags can take up to 24 hours to appear and they can’t be applied to legacy resources.
    </details>

10. Your online web store normally requires three EC2 instances to handle traffic but experiences a twofold increase in traffic for the two summer months. Which of the following approaches makes the most sense?
    - A. Run three on- demand instances 12 months per year and schedule six reserve instances.
    - B. Run three spot instances for the summer months and three reserve instances.
    - C. Run nine reserve instances for 12 months/year.
    - D. Run three reserve instances 12 months/year and purchase three scheduled reserve.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The most effective approach would be to run three reserve instances 12 months/year and
    </details>

11. Which of the following settings do you not need to provide when configuring a reserved instance?
    - A. Payment option.
    - B. Standard or Convertible RI.
    - C. Interruption policy.
    - D. Tenancy.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Interruption polices are relevant to spot instances, not reserved instances. Payment
    </details>

12. Your new web application requires multiple EC2 instances running 24/7 and you’re going to purchase reserved instances. Which of the following payment options is the most expensive when configuring a reserve instance?
    - A. All Upfront.
    - B. Partial Upfront.
    - C. No Upfront.
    - D. Monthly.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: No Upfront is the most expensive option. The more you pay up front, the lower the
    </details>

13. Which of the following benefits of containers such as Docker can significantly reduce your AWS compute costs? (Choose two.)
    - A. Containers can launch quickly.
    - B. Containers can deliver increased server density.
    - C. Containers make it easy to reliably replicate server environments.
    - D. Containers can run using less memory than physical machines.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: Containers are more dense and lightweight. Containers do tend to launch more quickly
    </details>

14. Which of the following is the best use of an EC2 reserved instance?
    - A. An application that will run continuously for six months straight.
    - B. An application that will run continuously for 36 months straight.
    - C. An application that runs only during local business hours.
    - D. An application that runs at unpredictable times and can survive unexpected shutdowns.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Standard reserve instances make the most sense when they need to be available 24/7 for at
    </details>

15. Which of the following describes “unused EC2 instances matching a particular set of launch specifications”?
    - A. Request type.
    - B. Spot instance interruption.
    - C. Spot fleet.
    - D. Spot instance pool.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: A spot instance pool is made up of unused EC2 instances. There are three request types:
    </details>

16. Which of the following best describes a spot instance interruption?
    - A. A spot instance interruption occurs when the spot price rises above your maximum.
    - B. A spot instance interruption is the termination of a spot instance when its workload.
    - C. A spot instance interruption occurs when a spot request is manually restarted.
    - D. A spot instance interruption is the result of a temporary outage in an AWS datacenter.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: A spot instance interruption occurs when the spot price rises above your maximum.
    </details>

17. Which of the following describes the maximum instances or vCPUs you want running?
    - A. Spot instance pool.
    - B. Target capacity.
    - C. Spot maximum.
    - D. Spot cap.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Target capacity represents the maximum instances you want running. A spot instance
    </details>

18. You need to make sure your EBS volumes are regularly backed up, but you’re afraid you’ll forget to remove older snapshot versions, leading to expensive data bloat. What’s the best solution to this problem?
    - A. Configure the EBS Lifecycle Manager.
    - B. Create a script that will regularly invoke the AWS CLI to prune older snapshots.
    - C. Configure an EBS Scheduled Reserved Instance.
    - D. Tie a string to your finger.
    - E. Configure an S3 Lifecycle configuration policy to remove old snapshots.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The EBS Lifecycle Manager can be configured to remove older EBS snapshots according
    </details>

19. Which of these AWS CLI commands will launch a spot fleet?
    - A. aws ec2 request- fleet - - spot- fleet- request- config file://.
    - B. aws ec2 spot- fleet - - spot- fleet- request- config file://.
    - C. aws ec2 launch- spot- fleet - - spot- fleet- request- config/ file://.
    - D. aws ec2 request- spot- fleet - - spot- fleet- request- config/ file://.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The command is request- spot- fleet. The - - spot- fleet- request- config
    </details>

20. Which of the following elements is not something you’d include in your spot fleet request?
    - A. Availability zone.
    - B. Target capacity.
    - C. Platform (the instance OS).
    - D. AMI.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: The availability zone, target capacity, and AMI are all elements of a complete spot fleet
    </details>
