# Solutions Architect Ch7: CloudTrail, CloudWatch, and AWS Config

1. You’ve configured CloudTrail to log all management events in all regions. Which of the fol- lowing API events will CloudTrail log? (Choose all that apply.)
    - A. Logging into the AWS Console.
    - B. Creating an S3 bucket from the web console.
    - C. Uploading an object to an S3 bucket.
    - D. Creating a subnet using the AWS CLI.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: Creating a bucket and subnet are API actions, regardless of whether they’re performed
    </details>

2. You’ve configured CloudTrail to log all read- only data events. Which of the following events will CloudTrail log?
    - A. Viewing all S3 buckets.
    - B. Uploading a file to an S3 bucket.
    - C. Downloading a file from an S3 bucket.
    - D. Creating a Lambda function.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Data events include S3 object- level activity and Lambda function executions. Download-
    </details>

3. Sixty days ago, you created a trail in CloudTrail to log read- only management events. Subse- quently someone deleted the trail. Where can you look to find out who deleted it? No other trails are configured.
    - A. The IAM user log.
    - B. The trail logs stored in S3.
    - C. The CloudTrail event history in the region where the trail was configured.
    - D. The CloudTrail event history in any region.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: CloudTrail stores 90 days of event history for each region, regardless of whether a trail
    </details>

4. What uniquely distinguishes two CloudWatch metrics that have the same name and are in the same namespace?
    - A. The region.
    - B. The dimension.
    - C. The timestamp.
    - D. The data point.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: CloudWatch uses dimensions to uniquely identify metrics with the same name and
    </details>

5. Which type of monitoring sends metrics to CloudWatch every five minutes?
    - A. Regular.
    - B. Detailed.
    - C. Basic.
    - D. High resolution.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C
      Explanation: Basic monitoring sends metrics every five minutes, whereas detailed monitoring sends
    </details>

6. You update a custom CloudWatch metric with the timestamp of 15:57:08 and a value of 3. You then update the same metric with the timestamp of 15:57:37 and a value of 6. Assuming the metric is a high- resolution metric, which of the following will CloudWatch do?
    - A. Record both values with the given timestamp.
    - B. Record the second value with the timestamp 15:57:37, overwriting the first value.
    - C. Record only the first value with the timestamp 15:57:08, ignoring the second value.
    - D. Record only the second value with the timestamp 15:57:00, overwriting the first value.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: CloudWatch can store high- resolution metrics at subminute resolution. Therefore, updat-
    </details>

7. How long does CloudWatch retain metrics stored at one- hour resolution?
    - A. 15 days.
    - B. 3 hours.
    - C. 63 days.
    - D. 15 months.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: Metrics stored at one- hour resolution age out after 15 months. Five- minute resolutions
    </details>

8. You want to use CloudWatch to graph the exact data points of a metric for the last hour. The metric is stored at five- minute resolution. Which statistic and period should you use?
    - A. The Sum statistic with a five- minute period.
    - B. The Average statistic with a one- hour period.
    - C. The Sum statistic with a one- hour period.
    - D. The Sample count statistic with a five- minute period.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: To graph a metric’s data points, specify the Sum statistic and set the period equal to the
    </details>

9. Which CloudWatch resource type stores log events?
    - A. Log group.
    - B. Log stream.
    - C. Metric filter.
    - D. CloudWatch Agent.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: CloudWatch uses a log stream to store log events from a single source. Log groups store
    </details>

10. The CloudWatch Agent on an instance has been sending application logs to a CloudWatch log stream for several months. How can you remove old log events without disrupting delivery of new log events? (Choose all that apply.)
    - A. Delete the log stream.
    - B. Manually delete old log events.
    - C. Set the retention of the log stream to 30 days.
    - D. Set the retention of the log group to 30 days.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, D
      Explanation: Every log stream must be in a log group. The retention period setting of a log group
    </details>

11. You created a trail to log all management events in all regions and send the trail logs to CloudWatch logs. You notice that some recent management events are missing from the log stream, but others are there. What are some possible reasons for this? (Choose all that apply.)
    - A. The missing events are greater than 256 KB in size.
    - B. The metric filter is misconfigured.
    - C. There’s a delay between the time the event occurs and the time CloudTrail streams the.
    - D. The IAM role that CloudTrail assumes is misconfigured.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A, C
      Explanation: CloudTrail will not stream events greater than 256 KB in size. There’s also a normal
    </details>

12. Two days ago, you created a CloudWatch alarm to monitor the VolumeReadOps on an EBS volume. Since then, the alarm has remained in an INSUFFICIENT_DATA state. What are some possible reasons for this? (Choose all that apply.)
    - A. The data points to monitor haven’t crossed the specified threshold.
    - B. The EBS volume isn’t attached to a running instance.
    - C. The evaluation period hasn’t elapsed.
    - D. The alarm hasn’t collected enough data points to alarm.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, D
      Explanation: If an EBS volume isn’t attached to a running instance, EBS won’t generate any met-
    </details>

13. You want a CloudWatch alarm to change state when four consecutive evaluation periods elapse with no data. How should you configure the alarm to treat missing data?
    - A. As Missing.
    - B. Breaching.
    - C. Not Breaching.
    - D. Ignore.
    - E. As Not Missing.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: To have CloudWatch treat missing data as exceeding the threshold, set the Treat Missing
    </details>

14. You’ve configured an alarm to monitor a metric in the AWS/EC2 namespace. You want CloudWatch to send you a text message and reboot an instance when an alarm is breaching. Which two actions should you configure in the alarm? (Choose two.)
    - A. SMS action.
    - B. Auto Scaling action.
    - C. Notification action.
    - D. EC2 action.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: CloudWatch can use the Simple Notification Service to send a text message. Cloud-
    </details>

15. In a CloudWatch alarm, what does the EC2 recover action do to the monitored instance?
    - A. Migrates the instance to a different host.
    - B. Reboots the instance.
    - C. Deletes the instance and creates a new one.
    - D. Restores the instance from a snapshot.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: A
      Explanation: The recover action is useful when there’s a problem with an instance that requires AWS
    </details>

16. You learn that an instance in the us- west- 1 region was deleted at some point in the past. To find out who deleted the instance and when, which of the following must be true?
    - A. The AWS Config configuration recorder must have been turned on in the region at the.
    - B. CloudTrail must have been logging write- only management events for all regions.
    - C. CloudTrail must have been logging IAM events.
    - D. The CloudWatch log stream containing the deletion event must not have been deleted.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: If CloudTrail were logging write- only management events in the same region as the
    </details>

17. Which of the following may be included in an AWS Config delivery channel? (Choose all that apply.)
    - A. A CloudWatch log stream.
    - B. The delivery frequency of the configuration snapshot.
    - C. An S3 bucket name.
    - D. An SNS topic ARN.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B, C, D
      Explanation: The delivery channel must include an S3 bucket name and may specify an SNS
    </details>

18. You configured AWS Config to monitor all your resources in the us- east- 1 region. After mak- ing several changes to the AWS resources in this region, you decided you want to delete the old configuration items. How can you accomplish this?
    - A. Pause the configuration recorder.
    - B. Delete the configuration recorder.
    - C. Delete the configuration snapshots.
    - D. Set the retention period to 30 days and wait for the configuration items to age out.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: D
      Explanation: You can’t delete configuration items manually, but you can have AWS Config delete them
    </details>

19. Which of the following metric math expressions can CloudWatch graph? (Choose all that apply.)
    - A. AVG(m1)- m1.
    - B. AVG(m1).
    - C. METRICS()/AVG(m1).
    - D. m1/m2.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: C, D
      Explanation: CloudWatch can graph only a time series. METRICS()/AVG(m1) and m1/m2 both
    </details>

20. You’ve configured an AWS Config rule to check whether CloudTrail is enabled. What could prevent AWS Config from evaluating this rule?
    - A. Turning off the configuration recorder.
    - B. Deleting the rule.
    - C. Deleting the configuration history for CloudTrail.
    - D. Failing to specify a frequency for periodic checks.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: Deleting the rule will prevent AWS Config from evaluating resources configurations
    </details>

21. Which of the following would you use to execute a Lambda function whenever an EC2 instance is launched?
    - A. CloudWatch Alarms.
    - B. EventBridge.
    - C. CloudTrail.
    - D. CloudWatch Metrics.

    <details markdown=1><summary markdown='span'>Answer</summary>
      Correct answer: B
      Explanation: EventBridge can take an action in response to an event, such as an EC2 instance launch.
    </details>
