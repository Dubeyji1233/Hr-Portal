# Solutions Architect Ch4: Amazon VPC

1. What is the range of allowed IPv4 prefix lengths for a VPC CIDR block?
    - A. /16 to /28.
    - B. /16 to /56.
    - C. /8 to /30.
    - D. /56 only.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The allowed range of prefix lengths for a VPC CIDR is between /16 and /28 inclusive. The
    </details>

2. You’ve created a VPC with the CIDR 192.168.16.0/24. You want to assign a secondary CIDR to this VPC. Which CIDR can you use?
    - A. 172.31.0.0/16.
    - B. 192.168.0.0/16.
    - C. 192.168.0.0/24.
    - D. 192.168.16.0/23.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: A secondary CIDR may come from the same RFC 1918 address range as the primary,
    </details>

3. You need to create two subnets in a VPC that has a CIDR of 10.0.0.0/16. Which of the fol- lowing CIDRs can you assign to one of the subnets while leaving room for an additional subnet? (Choose all that apply.)
    - A. 10.0.0.0/24.
    - B. 10.0.0.0/8.
    - C. 10.0.0.0/16.
    - D. 10.0.0.0/23.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Options A and D (10.0.0.0/24 and 10.0.0.0/23) are within the VPC CIDR and leave
    </details>

4. What is the relationship between a subnet and an availability zone?
    - A. A subnet can exist in multiple availability zones.
    - B. An availability zone can have multiple subnets.
    - C. An availability zone can have only one subnet.
    - D. A subnet’s CIDR is derived from its availability zone.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Multiple subnets may exist in a single availability zone. A subnet cannot span avail-
    </details>

5. Which is true regarding an elastic network interface?
    - A. It must have a private IP address from the subnet that it resides in.
    - B. It cannot exist independently of an instance.
    - C. It can be connected to multiple subnets.
    - D. It can have multiple IP addresses from different subnets.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Every ENI must have a primary private IP address. It can have secondary IP addresses,
    </details>

6. Which of the following statements is true of security groups?
    - A. Only one security group can be attached to an ENI.
    - B. A security group must always be attached to an ENI.
    - C. A security group can be attached to a subnet.
    - D. Every VPC contains a default security group.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Each VPC contains a default security group that can’t be deleted. You can create a secu-
    </details>

7. How does an NACL differ from a security group?
    - A. An NACL is stateless.
    - B. An NACL is stateful.
    - C. An NACL is attached to an ENI.
    - D. An NACL can be associated with only one subnet.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: An NACL is stateless, meaning it doesn’t track a connection state. Every inbound rule
    </details>

8. What is an Internet gateway?
    - A. A resource that grants instances in multiple VPCs’ Internet access.
    - B. An implied router.
    - C. A physical router.
    - D. A VPC resource with no management IP address.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: An Internet gateway has no management IP address. It can be associated with only one
    </details>

9. What is the destination for a default IPv4 route?
    - A. 0.0.0.0/0.
    - B. ::0/0.
    - C. An Internet gateway.
    - D. The IP address of the implied router.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The destination 0.0.0.0/0 matches all IP prefixes and hence covers all publicly accessible
    </details>

10. You create a new route table in a VPC but perform no other configuration on it. You then create a new subnet in the same VPC. Which route table will your new subnet be associ- ated with?
    - A. The main route table.
    - B. The route table you created.
    - C. The default route table.
    - D. None of these.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Every subnet is associated with the main route table by default. You can explicitly
    </details>

11. You create a Linux instance and have AWS automatically assign a private IP address but not a public IP address. What will happen when you stop and restart the instance?
    - A. You won’t be able to establish an SSH session directly to the instance from the Internet.
    - B. The instance won’t be able to access the Internet.
    - C. The instance will receive the same private IP address.
    - D. The instance will be unable to reach other instances in its subnet.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: An instance must have a public IP address to be directly reachable from the Internet. The
    </details>

12. How can you assign a public IP address to a running instance that doesn’t have one?
    - A. Allocate an ENI and associate it with the instance’s primary EIP.
    - B. Allocate an EIP and associate it with the instance’s primary ENI.
    - C. Configure the instance to use an automatically assigned public IP.
    - D. Allocate an EIP and change the private IP address of the instance’s ENI to match.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Assigning an EIP to an instance is a two- step process. First you must allocate an EIP, and
    </details>

13. When an instance with an automatically assigned public IP sends a packet to another instance’s EIP, what source address does the destination instance see?
    - A. The public IP.
    - B. The EIP.
    - C. The private IP.
    - D. 0.0.0.0.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Internet- bound traffic from an instance with an automatically assigned public IP will
    </details>

14. Why must a NAT gateway reside in a different subnet than an instance that uses it?
    - A. Both must use different default gateways.
    - B. Both must use different NACLs.
    - C. Both must use different security groups.
    - D. The NAT gateway requires a public interface and a private interface.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The NAT gateway’s default route must point to an Internet gateway, and the instance’s
    </details>

15. Which of the following is a difference between a NAT instance and a NAT gateway?
    - A. There are different NAT gateway types.
    - B. A NAT instance scales automatically.
    - C. A NAT gateway can span multiple availability zones.
    - D. A NAT gateway scales automatically.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: A NAT gateway is a VPC resource that scales automatically to accommodate increased
    </details>

16. Which VPC resource performs network address translation?
    - A. Internet gateway.
    - B. Route table.
    - C. EIP.
    - D. ENI.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: An Internet gateway performs NAT for instances that have a public IP address. A route
    </details>

17. What must you do to configure a NAT instance after creating it?
    - A. Disable the source/destination check on its ENI.
    - B. Enable the source/destination check on its ENI.
    - C. Create a default route in its route table with a NAT gateway as the target.
    - D. Assign a primary private IP address to the instance.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: The AWS Certificate Manager (when used as part of a CloudFront distribution) can
    </details>

18. Which of the following is true regarding VPC peering?
    - A. Transitive routing is not supported.
    - B. A VPC peering connection requires a public IP address.
    - C. You can peer up to three VPCs using a single peering connection.
    - D. You can use a peering connection to share an Internet gateway among multiple VPCs.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: As of this writing, retrieving Glacier Deep Archive data will take no larger than 12 hours.
    </details>

19. You’ve created one VPC peering connection between two VPCs. What must you do to use this connection for bidirectional instance- to- instance communication? (Choose all that apply.)
    - A. Create two routes with the peering connection as the target.
    - B. Create only one default route with the peering connection as the target.
    - C. Create another peering connection between the VPCs.
    - D. Configure the instances’ security groups correctly.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Direct Connect can provide fast network connections to AWS, but it’s very expensive and
    </details>

20. Which of the following can perform stateful traffic filtering? (Choose two.)
    - A. Security groups.
    - B. NACLs.
    - C. AWS Network Firewall.
    - D. AWS Transit Gateway.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: FSx for Lustre and Elastic File System are primarily designed for access from Linux file-
    </details>
