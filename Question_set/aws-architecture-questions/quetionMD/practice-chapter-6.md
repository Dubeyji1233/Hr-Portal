# Solutions Architect Ch6: Authentication and Authorization

1. Which of the following is the greatest risk posed by using your AWS account root user for day- to- day operations?
    - A. There would be no easy way to control resource usage by project or class.
    - B. There would be no effective limits on the effect of an action, making it more likely for.
    - C. Since root has full permissions over your account resources, an account compromise at.
    - D. It would make it difficult to track which account user is responsible for specific actions.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Although each of the other options represents possible concerns, none of them carries
    </details>

2. You’re trying to create a custom IAM policy to more closely manage access to components in your application stack. Which of the following syntax- related statements is a correct descrip- tion of IAM policies?
    - A. The Action element refers to the way IAM will react to a request.
    - B. The * character applies an element globally- as broadly as possible.
    - C. The Resource element refers to the third- party identities that will be allowed to access.
    - D. The Effect element refers to the anticipated resource state after a request is granted.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: The * character does, indeed, represent global application. The Action element refers to
    </details>

3. Which of the following will- when executed on its own- prevent an IAM user with no exist- ing policies from launching an EC2 instance? (Choose three.)
    - A. Attach no policies to the user.
    - B. Attach two policies to the user, with one policy permitting full EC2 access and the other.
    - C. Attach a single policy permitting the user to create S3 buckets.
    - D. Attach the AdministratorAccess policy.
    - E. Associate an IAM action statement blocking all EC2 access to the user’s account.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B, C
      Explanation: Unless there’s a policy that explicitly allows an action, it will be denied. Therefore,
    </details>

4. Which of the following are important steps for securing IAM user accounts? (Choose two.)
    - A. Never use the account to perform any administration operations.
    - B. Enable multifactor authentication (MFA).
    - C. Assign a long and complex password.
    - D. Delete all access keys.
    - E. Insist that your users access AWS resources exclusively through the AWS CLI.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: If you don’t perform any administration operations with regular IAM users, then there
    </details>

5. To reduce your exposure to possible attacks, you’re auditing the active access keys associated with your account. Which of the following AWS CLI commands can tell you whether a speci- fied access key is still being used?
    - A. aws iam get- access- key- used -access- key- id <key_ID>.
    - B. aws iam - - get- access- key- last- used access- key- id <key_ID>.
    - C. aws iam get- access- key- last- used access- last- key- id <key_ID>.
    - D. aws iam get- access- key- last- used -- access- key- id <key_ID>.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The top- level command is iam, and the correct subcommand is
    </details>

6. You’re looking to reduce the complexity and tedium of AWS account administration. Which of the following is the greatest benefit of organizing your users into groups?
    - A. It enhances security by consolidating resources.
    - B. It simplifies the management of user permissions.
    - C. It allows for quicker response times to service interruptions.
    - D. It simplifies locking down the root user.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: IAM groups are primarily about simplifying administration. They have no direct impact
    </details>

7. During an audit of your authentication processes, you enumerate a number of identity types and want to know which of them might fit the category of “trusted identity” and require deeper investigation. Which of these is not considered a trusted entity in the context of IAM roles?
    - A. A web identity authenticating with Google.
    - B. An identity coming through a SAML- based federated provider.
    - C. An identity using an X.509 certificate.
    - D. A web identity authenticating with Amazon Cognito.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: X.509 certificates are used for encrypting SOAP requests, not authentication. The other
    </details>

8. Your company is bidding for a contract with a U.S. government agency that demands any cryptography modules used on the project be compliant with government standards. Which of the following AWS services provides virtual hardware devices for managing encryption infrastructure that’s FIPS 140- 2 compliant?
    - A. AWS CloudHSM.
    - B. AWS Key Management Service.
    - C. AWS Security Token Service.
    - D. AWS Secrets Manager.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: AWS CloudHSM provides encryption that’s FIPS 140- 2 compliant. Key Management
    </details>

9. Which of the following is the best tool for authenticating access to a VPC- based Microsoft SharePoint farm?
    - A. Amazon Cognito.
    - B. AWS Directory Service for Microsoft Active Directory.
    - C. AWS Secrets Manager.
    - D. AWS Key Management Service.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: AWS Directory Service for Microsoft Active Directory provides Active Directory authen-
    </details>

10. What is the function of Amazon Cognito identity pools?
    - A. Gives your application users temporary, controlled access to other services in your.
    - B. Adds user sign- up and sign- in to your applications.
    - C. Incorporates encryption infrastructure into your application life cycle.
    - D. Delivers up- to- date credentials to authenticate RDS database requests.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Identity pools provide temporary access to defined AWS services to your application
    </details>

11. An employee with access to the root user on your AWS account has just left your company. Since you can’t be 100 percent sure that the former employee won’t try to harm your company, which of the following steps should you take? (Choose three.)
    - A. Change the password and MFA settings for the root account.
    - B. Delete and re- create all existing IAM policies.
    - C. Change the passwords for all your IAM users.
    - D. Delete the former employee’s own IAM user (within the company account).
    - E. Immediately rotate all account access keys.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D, E
      Explanation: Options A, D, and E are appropriate steps. Your IAM policies will be as effective as
    </details>

12. You need to create a custom IAM policy to give one of your developers limited access to your DynamoDB resources. Which of the following elements will not play any role in crafting an IAM policy?
    - A. Action.
    - B. Region.
    - C. Effect.
    - D. Resource.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: IAM policies are global- they’re not restricted to any one region. Policies do, however,
    </details>

13. Which of the following are necessary steps for creating an IAM role? (Choose two.)
    - A. Define the action.
    - B. Select at least one policy.
    - C. Define a trusted entity.
    - D. Define the consumer application.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C
      Explanation: IAM roles require a defined trusted entity and at least one policy. However, the relevant
    </details>

14. Which of the following uses authentication based on AWS Security Token Service (STS) tokens?
    - A. Policies.
    - B. Users.
    - C. Groups.
    - D. Roles.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: STS tokens are used as temporary credentials to external identities for resource access to
    </details>

15. What format must be used to write an IAM policy?
    - A. HTML.
    - B. Key/value pairs.
    - C. JSON.
    - D. XML.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Policies must be written in JSON format.
    </details>

16. If you need to allow a user full control over EC2 instance resources, which two of the follow- ing must be included in the policy you create? (Choose two.)
    - A. "Target": "ec2:*".
    - B. "Action": "ec2:*".
    - C. "Resource": "ec2:*".
    - D. "Effect": "Allow".
    - E. "Effect": "Permit".

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: The correct Resource line would read "Resource": "*". And the correct Action line
    </details>

17. What is the function of Amazon Cognito user pools?
    - A. Gives your application users temporary, controlled access to other services in your.
    - B. Adds user sign- up and sign- in to your applications.
    - C. Incorporates encryption infrastructure into your application life cycle.
    - D. Delivers up- to- date credentials to authenticate RDS database requests.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: User pools provide sign- up and sign- in for your application’s users. Temporary access to
    </details>

18. Which of the following best describe the “managed” part of AWS Managed Microsoft AD? (Choose two.)
    - A. Integration with on- premises AD domains is possible.
    - B. AD domain controllers are launched in two availability zones.
    - C. Data is automatically replicated.
    - D. Underlying AD software is automatically updated.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: An AWS managed service takes care of all underlying infrastructure management
    </details>

19. Which of the following steps are part of the access key rotation process? (Choose three.)
    - A. Monitor the use of your new keys.
    - B. Monitor the use of old keys.
    - C. Deactivate the old keys.
    - D. Delete the old keys.
    - E. Confirm the status of your X.509 certificate.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C, D
      Explanation: Options B, C, and D are all parts of the key rotation process. In this context, key
    </details>

20. What tool will allow an Elastic Container Service task to access container images it might need that are being maintained in your account’s Elastic Container Registry?
    - A. An IAM role.
    - B. An IAM policy.
    - C. An IAM group.
    - D. An AIM access key.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: You attach IAM roles to services in order to give them permissions over resources in other
    </details>
