output "cloudtrail_bucket_name" {
  description = "S3 bucket name storing CloudTrail audit logs"
  value       = aws_s3_bucket.cloudtrail_logs.id
}

output "cloudtrail_bucket_arn" {
  description = "ARN of the CloudTrail S3 bucket"
  value       = aws_s3_bucket.cloudtrail_logs.arn
}

output "cloudtrail_arn" {
  description = "ARN of the CloudTrail trail"
  value       = aws_cloudtrail.securewatch.arn
}

output "guardduty_detector_id" {
  description = "GuardDuty detector ID — needed for Module 5 SIEM integration"
  value       = aws_guardduty_detector.securewatch.id
}

output "sns_topic_arn" {
  description = "SNS security alerts topic ARN"
  value       = aws_sns_topic.security_alerts.arn
}

output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}