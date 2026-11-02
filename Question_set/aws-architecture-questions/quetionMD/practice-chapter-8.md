# Solutions Architect Ch8: Route 53 and CloudFront

1. Which of the following describes the function of a name server?
    - A. Translating human- readable domain names into IP addresses.
    - B. Registering domain names with ICANN.
    - C. Registering domain names with VeriSign.
    - D. Applying routing policies to network packets.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Option A is the correct answer. Name servers resolve IP addresses from domain names,
    </details>

2. Your organization is planning a new website and you’re putting together all the pieces of information you’ll need to complete the project. Which of the following describes a domain?
    - A. An object’s FQDN.
    - B. Policies controlling the way remote requests are resolved.
    - C. One or more servers, data repositories, or other digital resources identified by a single.
    - D. A label used to direct network requests to a domain’s resources.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: A domain is a set of resources identified by a single domain name. FQDN stands for fully
    </details>

3. You need to decide which kind of website name will best represent its purpose. Part of that task will involve choosing a top- level domain (TLD). Which of the following is an example of a TLD?
    - A. amazon.com/documentation/.
    - B. aws.
    - C. amazon.
    - D. .com.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: The rightmost section of an FQDN address is the TLD. aws. would be a subdomain or
    </details>

4. Which of the following is the name of a record type- as used- in a zone file?
    - A. CNAME (canonical name).
    - B. TTL (time to live).
    - C. Record type.
    - D. Record data.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: CNAME is a record type. TTL, record type, and record data are all configuration ele-
    </details>

5. Which of the following DNS record types should you use to associate a domain name with an IP address?
    - A. NS.
    - B. SOA.
    - C. A.
    - D. CNAME.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: An A record maps a hostname to an IPv4 address. NS records identify name servers. SOA
    </details>

6. Which of the following are services provided by Amazon Route 53? (Choose three.)
    - A. Domain registration.
    - B. Content delivery network.
    - C. Health checks.
    - D. DNS management.
    - E. Secure and fast direct network connections to an AWS VPC.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C, D
      Explanation: Route 53 provides domain registration, health checks, and DNS management.
    </details>

7. For regulatory compliance, your application may only provide data to requests coming from the United States. Which of the following routing policies can be configured to do this?
    - A. Simple.
    - B. Latency.
    - C. Geolocation.
    - D. Multivalue.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Geolocation can control routing by the geographic origin of the request. The simple
    </details>

8. Your web application is hosted within multiple AWS regions. Which of the following routing policies will ensure the fastest possible access for your users?
    - A. Latency.
    - B. Weighted.
    - C. Geolocation.
    - D. Failover.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Latency selects the available resource with the lowest latency. Weighted policies route
    </details>

9. You’re testing three versions of a new application, with each version running on its own server and the current production version on a fourth server. You want to route 15 percent of your total traffic to each of the test servers and route the remaining 85 percent of traffic to the production server. Which routing policy will you use?
    - A. Failover.
    - B. Weighted.
    - C. Latency.
    - D. Geolocation.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Weighted policies route among multiple resources by percentage. Failover incorporates
    </details>

10. You have production infrastructure in one region sitting behind one DNS domain, and for disaster recovery purposes, you have parallel infrastructure on standby in a second AWS region behind a second domain. Which routing policy will automate the switchover in the event of a failure in the production system?
    - A. Latency.
    - B. Weighted.
    - C. Geolocation.
    - D. Failover.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Failover incorporates backup resources for higher availability. Latency selects the avail-
    </details>

11. Which of the following kinds of hosted zones are real options within Route 53? (Choose two.)
    - A. Public.
    - B. Regional.
    - C. VPC.
    - D. Private.
    - E. Hybrid.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Public and private hosting zones are real options. Regional, hybrid, and VPC zones
    </details>

12. Which of the following actions will you need to perform to transfer a domain from an external registrar to Route 53? (Choose two.)
    - A. Unlock the domain transfer setting on the external registrar admin page.
    - B. Request an authorization code from the external registrar.
    - C. Copy the name server addresses from Route 53 to the external registrar admin page.
    - D. Create a hosted zone CNAME record set.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, B
      Explanation: To transfer a domain, you’ll need to make sure the domain isn’t set to locked. You’ll
    </details>

13. Which of the following actions will you need to perform to use Route 53 to manage a domain that’s being hosted on an external registrar?
    - A. Request an authorization code from the external registrar.
    - B. Copy the name server addresses from Route 53 to the external registrar admin page.
    - C. Create a hosted zone CNAME record set.
    - D. Unlock the domain transfer setting on the external registrar admin page.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: You can enable remotely registered domains on Route 53 by copying name server
    </details>

14. Your multiserver application has been generating quality- related complaints from users and your logs show some servers are underused and others have been experiencing intermittent failures. How do Route 53 health checks test for the health of a resource so that a failover policy can direct your users appropriately?
    - A. It periodically tries to load the index.php page.
    - B. It periodically tries to load the index.html page.
    - C. It periodically tries to load a specified web page.
    - D. It periodically tries to log into the resource using SSH.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: You specify the web page that you want used for testing when you configure your health
    </details>

15. Which of the following most accurately describes the difference between geolocation and geoproximity routing policies?
    - A. Geoproximity policies specify geographic areas by their relationship either to a.
    - B. Geolocation policies specify geographic areas by their relationship either to a particular.
    - C. Geolocation policies will direct traffic to the resource you identify as primary as long as.
    - D. Geolocation policies use a health check configuration routing to make a deployment.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Geoproximity is about precisely pinpointing users, whereas geolocation uses geopolitical
    </details>

16. Which of the following are challenges that CloudFront is well positioned to address? (Choose two.)
    - A. A heavily used website providing media downloads for a global audience.
    - B. An S3 bucket with large media files used by workers on your corporate campus.
    - C. A file server accessed through a corporate VPN.
    - D. A popular website with periodically changing content.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: CloudFront is optimized for handling heavy download traffic and for caching website
    </details>

17. Which of the following is not a permitted origin for a CloudFront distribution?
    - A. Amazon S3 bucket.
    - B. AWS MediaPackage channel endpoint.
    - C. API Gateway endpoint.
    - D. Web server.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: API Gateway is used to generate custom client SDKs for your APIs to connect your back-
    </details>

18. What’s the best way to control the costs your CloudFront distribution incurs?
    - A. Select a price class that maintains copies in only a limited subset of CloudFront’s edge.
    - B. Configure a custom SSL certificate to restrict access to HTTPS requests only.
    - C. Disable the use of Alternate Domain Names (CNAMES) for your distribution.
    - D. Enable Compress Objects Automatically for your distribution.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: Choosing a price class offering limited distribution is the best way to reduce costs. Non-
    </details>

19. Which of the following is not necessarily a direct benefit of using a CloudFront distribution?
    - A. User requests from an edge location that’s recently received the same request will be.
    - B. CloudFront distributions can be directly mapped to Route 53 hosted zones.
    - C. All user requests will be delivered with lower latency.
    - D. You can incorporate free encryption certificates into your infrastructure.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Not every CloudFront distribution is optimized for low- latency service. Requests of an
    </details>

20. Which of the following content types is the best fit for a Real- Time Messaging Protocol (RTMP) distribution?
    - A. Amazon Elastic Transcoder-based videos.
    - B. S3- based videos.
    - C. Streaming videos.
    - D. A mix of text and media- rich digital content.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: RTMP distributions can manage content only from S3 buckets. RTMP is intended for the
    </details>
