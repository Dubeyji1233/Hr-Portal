# Solutions Architect Ch2: Compute Services

1. You need to deploy multiple EC2 Linux instances that will provide your company with virtual private networks (VPNs) using software called OpenVPN. Which of the following will be the most efficient solutions? (Choose two.)
    - A. Select a regular Linux AMI and bootstrap it using user data that will install and con-.
    - B. Search the community AMIs for an official AMI provided and supported by the Open-.
    - C. Search the AWS Marketplace to see whether there’s an official AMI provided and sup-.
    - D. Select a regular Linux AMI and SSH to manually install and configure the OpenVPN.
    - E. Create a site- to- site VPN connection from the wizard in the AWS VPC dashboard.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: Many third- party companies maintain official and supported AMIs running their soft-
    </details>

2. As part of your company’s long- term cloud migration strategy, you have a VMware virtual machine in your local infrastructure that you’d like to copy to your AWS account and run as an EC2 instance. Which of the following will be necessary steps? (Choose two.)
    - A. Import the virtual machine to your AWS region using a secure SSH tunnel.
    - B. Import the virtual machine using VM Import/Export.
    - C. Select the imported VM from among your private AMIs and launch an instance.
    - D. Select the imported VM from the AWS Marketplace AMIs and launch an instance.
    - E. Use the AWS CLI to securely copy your virtual machine image to an S3 bucket within.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: The VM Import/Export tool handles the secure and reliable transfer for a virtual
    </details>

3. Your AWS CLI command to launch an AMI as an EC2 instance has failed, giving you an error message that includes InvalidAMIID.NotFound. What of the following is the most likely cause?
    - A. You haven’t properly configured the ~/.aws/config file.
    - B. The AMI is being updated and is temporarily unavailable.
    - C. Your key pair file has been given the wrong (overly permissive) permissions.
    - D. The AMI you specified exists in a different region than the one you’ve currently.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: AMIs are specific to a single AWS region and cannot be deployed into any other region.
    </details>

4. The sensitivity of the data your company works with means that the instances you run must be secured through complete physical isolation. What should you specify as you configure a new instance?
    - A. Dedicated Host tenancy.
    - B. Shared tenancy.
    - C. Dedicated Instance tenancy.
    - D. Isolated tenancy.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Only Dedicated Host tenancy offers full isolation. Shared tenancy instances will often
    </details>

5. Normally, two instances running m5.large instance types can handle the traffic accessing your online e- commerce site, but you know that you will face short, unpredictable periods of high demand. Which of the following choices should you implement? (Choose two.)
    - A. Configure autoscaling.
    - B. Configure load balancing.
    - C. Purchase two m5.large instances on the spot market and as many on- demand instances.
    - D. Shut down your m5.large instances and purchase instances using a more robust instance.
    - E. Purchase two m5.large reserve instances and as many on- demand instances as necessary.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, E
      Explanation: Reserve instances will give you the best price for instances you know will be running
    </details>

6. Which of the following use cases would be most cost effective if run using spot market instances?
    - A. Your e- commerce website is built using a publicly available AMI.
    - B. You provide high- end video rendering services using a fault- tolerant process that can.
    - C. You’re running a backend database that must be reliably updated to keep track of criti-.
    - D. Your deployment runs as a static website on S3.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Spot market instances can be shut down with only a minimal (two- minute) warning, so
    </details>

7. In the course of a routine infrastructure audit, your organization discovers that some of your running EC2 instances are not configured properly and must be updated. Which of the fol- lowing configuration details cannot be changed on an existing EC2 instance?
    - A. AMI.
    - B. Instance type.
    - C. Security group.
    - D. Public IP address.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: You can edit or even add or remove security groups from running instances and the
    </details>

8. For an account with multiple resources running as part of multiple projects, which of the following key/value combination examples would make for the most effective identification convention for resource tags?
    - A. servers:server1.
    - B. project1:server1.
    - C. EC2:project1:server1.
    - D. server1:project1.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The first of two (and not three) strings in a resource tag is the key- the group to which
    </details>

9. Which of the following EBS options will you need to keep your data- hungry application that requires up to 20,000 IOPS happy?
    - A. Cold HDD.
    - B. General- purpose SSD.
    - C. Throughput- optimized HDD.
    - D. Provisioned- IOPS SSD.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Provisioned- IOPS SSD volumes are currently the only type that comes close to 20,000
    </details>

10. Your organization needs to introduce Auto Scaling to its infrastructure and needs to gen- erate a “golden image” AMI from an existing EBS volume. This image will need to be shared among multiple AWS accounts belonging to your organization. Which of the following steps will get you there? (Choose three.)
    - A. Create an image from a detached EBS volume, use it to create a snapshot, select your.
    - B. Create a snapshot of the EBS root volume you need, use it to create an image, select your.
    - C. Create an image from the EBS volume attached to the instance, select your new AMI.
    - D. Search the AWS Marketplace for the appropriate image and use it for your launch.
    - E. Import the snapshot of an EBS root volume from a different AWS account, use it to.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C, E
      Explanation: Options B, C, and E are steps necessary for creating and sharing such an image.
    </details>

11. Which of the following are benefits of instance store volumes? (Choose two.)
    - A. Instance volumes are physically attached to the server that’s hosting your instance,.
    - B. Instance volumes can be used to store data even after the instance is shut down.
    - C. The use of instance volumes does not incur costs (beyond those for the instance itself).
    - D. You can set termination protection so that an instance volume can’t be accidentally.
    - E. Instance volumes are commonly used as a base for the creation of AMIs.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: The fact that instance volumes are physically attached to the host server and add
    </details>

12. According to default behavior (and AWS recommendations), which of the following IP addresses could be assigned as the private IP for an EC2 instance? (Choose two.)
    - A. 54.61.211.98.
    - B. 23.176.92.3.
    - C. 172.17.23.43.
    - D. 10.0.32.176.
    - E. 192.140.2.118.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: By default, EC2 uses the standard address blocks for private subnets, so all private
    </details>

13. You need to restrict access to your EC2 instance- based application to only certain clients and only certain targets. Which three attributes of an incoming data packet are used by a security group to determine whether it should be allowed through? (Choose three.)
    - A. Network port.
    - B. Source address.
    - C. Datagram header size.
    - D. Network protocol.
    - E. Destination address.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, D
      Explanation: Ports and source and destinations addresses are considered by security group rules.
    </details>

14. How are IAM roles commonly used to ensure secure resource access in relation to EC2 instances?
    - A. A role can assign processes running on the EC2 instance itself permission to access other.
    - B. A user can be given permission to authenticate as a role and access all associated.
    - C. A role can be associated with individual instance- based processes (Linux instances only),.
    - D. A role can give users and resources permission to access the EC2 instance.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: IAM roles define how resources access other resources. Users cannot authenticate as an
    </details>

15. You have an instance running within a private subnet that needs external network access to receive software updates and patches. Which of the following can securely provide that access from a public subnet within the same VPC? (Choose two.)
    - A. Internet gateway.
    - B. NAT instance.
    - C. Virtual private gateway.
    - D. NAT gateway.
    - E. VPN.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: NAT instances and NAT gateways are AWS tools for safely routing traffic between
    </details>

16. What do you have to do to securely authenticate to the GUI console of a Windows EC2 session?
    - A. Use the private key of your key pair to initiate an SSH tunnel session.
    - B. Use the public key of your key pair to initiate an SSH tunnel session.
    - C. Use the public key of your key pair to retrieve the password you’ll use to log in.
    - D. Use the private key of your key pair to retrieve the password you’ll use to log in.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The client computer in an encrypted operation must always use the private key to authen-
    </details>

17. Your application deployment includes multiple EC2 instances that need low- latency connec- tions to each other. Which of the following AWS tools will allow you to locate EC2 instances closer to each other to reduce network latency?
    - A. Load balancing.
    - B. Placement groups.
    - C. AWS Systems Manager.
    - D. AWS Fargate.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Placement groups allow you to specify where your EC2 instances will live. Load balancing
    </details>

18. To save configuration time and money, you want your application to run only when net- work events trigger it but shut down immediately after. Which of the following will do that for you?
    - A. AWS Lambda.
    - B. AWS Elastic Beanstalk.
    - C. Amazon Elastic Container Service (ECS).
    - D. Auto Scaling.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Lambda can be used as such a trigger. Beanstalk launches and manages infrastructure for
    </details>

19. Which of the following will allow you to quickly copy a virtual machine image from your local infrastructure to your AWS VPC?
    - A. AWS Simple Storage Service (S3).
    - B. AWS Snowball.
    - C. VM Import/Export.
    - D. AWS Direct Connect.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: VM Import/Export will do this. S3 buckets are used to store an image, but they’re not
    </details>

20. You’ve configured an EC2 Auto Scaling group to use a launch configuration to provision and install an application on several instances. You now need to reconfigure Auto Scaling to install an additional application on new instances. Which of the following should you do?
    - A. Modify the launch configuration.
    - B. Create a launch template and configure the Auto Scaling group to use it.
    - C. Modify the launch template.
    - D. Modify the CloudFormation template.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: You can modify a launch template by creating a new version of it; however, the question
    </details>

21. You create an Auto Scaling group with a minimum group size of 3, a maximum group size of 10, and a desired capacity of 5. You then manually terminate two instances in the group. Which of the following will Auto Scaling do?
    - A. Create two new instances.
    - B. Reduce the desired capacity to 3.
    - C. Nothing.
    - D. Increment the minimum group size to 5.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Auto Scaling strives to maintain the number of instances specified in the desired capacity
    </details>

22. You’re running an application that receives a spike in traffic on the first day of every month. You want to configure Auto Scaling to add more instances before the spike begins and then add additional instances in proportion to the CPU utilization of each instance. Which of the following should you implement? (Choose all that apply.)
    - A. Target tracking policies.
    - B. Scheduled actions.
    - C. Step scaling policies.
    - D. Simple scaling policies.
    - E. Load balancing.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: Scheduled actions can adjust the minimum and maximum group sizes and the desired
    </details>

23. As part of your new data backup protocols, you need to manually take EBS snapshots of sev- eral hundred volumes. Which type of Systems Manager document enables you to do this?
    - A. Command.
    - B. Automation.
    - C. Policy.
    - D. Manual.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Automation documents let you perform actions against your AWS resources, including
    </details>

24. You want to launch and manage a complex microservices container workload in AWS but you want to avoid as many configuration headaches as possible, You figure you’ll be fine with whatever defaults you’re offered. Which of these platforms is your best choice?
    - A. Amazon Elastic Kubernetes Service.
    - B. AWS Fargate.
    - C. Amazon EKS Distro.
    - D. Amazon Elastic Container Service.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Fargate is a service that uses either ECS or EKS infrastructure under the hood, but actu-
    </details>
