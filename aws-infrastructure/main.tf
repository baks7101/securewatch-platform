# =============================================================================
# SecureWatch Platform - AWS Security Infrastructure
# Designed to mirror real NHS/healthcare security requirements
# Covers: CloudTrail audit logging, GuardDuty threat detection,
# encrypted S3 storage, SNS alerting, CloudWatch event routing
# Compliance context: GDPR Article 32, NHS DSP Toolkit
# =============================================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Get current AWS account details
data "aws_caller_identity" "current" {}

# =============================================================================
# RANDOM SUFFIX
# S3 bucket names must be globally unique across ALL of AWS worldwide.
# We add a random 4-character suffix to guarantee uniqueness.
# =============================================================================
resource "random_id" "suffix" {
  byte_length = 4
}

# =============================================================================
# S3 BUCKET — CLOUDTRAIL LOG STORAGE
# S3 = Simple Storage Service. Think of it as a secure filing cabinet
# in the cloud where CloudTrail drops its log files every few minutes.
#
# Security controls applied (all required by NHS DSP Toolkit):
# - Encryption at rest (AES256)
# - Versioning enabled (protects against accidental deletion)
# - All public access blocked (logs must never be public)
# - Bucket policy restricts write access to CloudTrail service only
# =============================================================================
resource "aws_s3_bucket" "cloudtrail_logs" {
  bucket        = "${var.project_name}-cloudtrail-${random_id.suffix.hex}"
  force_destroy = true

  tags = {
    Name        = "SecureWatch CloudTrail Logs"
    Environment = "Dev"
    Project     = "SecureWatch"
    Compliance  = "NHS-DSP-Toolkit"
  }
}

resource "aws_s3_bucket_public_access_block" "cloudtrail_logs" {
  bucket                  = aws_s3_bucket.cloudtrail_logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "cloudtrail_logs" {
  bucket = aws_s3_bucket.cloudtrail_logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_policy" "cloudtrail_logs" {
  bucket     = aws_s3_bucket.cloudtrail_logs.id
  depends_on = [aws_s3_bucket_public_access_block.cloudtrail_logs]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AWSCloudTrailAclCheck"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:GetBucketAcl"
        Resource = aws_s3_bucket.cloudtrail_logs.arn
      },
      {
        Sid    = "AWSCloudTrailWrite"
        Effect = "Allow"
        Principal = {
          Service = "cloudtrail.amazonaws.com"
        }
        Action   = "s3:PutObject"
        Resource = "${aws_s3_bucket.cloudtrail_logs.arn}/AWSLogs/${data.aws_caller_identity.current.account_id}/*"
        Condition = {
          StringEquals = {
            "s3:x-amz-acl" = "bucket-owner-full-control"
          }
        }
      }
    ]
  })
}

# =============================================================================
# CLOUDTRAIL
# Records every API call made in your AWS account — who did what, when,
# from where. This is your audit trail for GDPR and NHS DSP Toolkit.
#
# Key settings:
# - Multi-region: captures activity across ALL regions not just London
# - Log file validation: detects if logs are tampered with
# - Global service events: captures IAM, Route53 etc
# =============================================================================
resource "aws_cloudtrail" "securewatch" {
  name                          = "securewatch-trail"
  s3_bucket_name                = aws_s3_bucket.cloudtrail_logs.id
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_log_file_validation    = true

  tags = {
    Name       = "SecureWatch Audit Trail"
    Project    = "SecureWatch"
    Compliance = "GDPR-Article32"
  }

  depends_on = [aws_s3_bucket_policy.cloudtrail_logs]
}

# =============================================================================
# GUARDDUTY — THREAT DETECTION
# GuardDuty is AWS's intelligent threat detection service.
# It analyses CloudTrail, DNS logs, and VPC flow logs using ML models
# to identify threats that rules-based systems would miss.
#
# What it detects relevant to healthcare:
# - Unusual API calls (potential data exfiltration)
# - Cryptocurrency mining (compromised instance)
# - Reconnaissance activity (attacker mapping your environment)
# - Credential compromise (unusual login locations/times)
# - S3 data exfiltration attempts (patient record theft)
# =============================================================================
resource "aws_guardduty_detector" "securewatch" {
  enable = true

  datasources {
    s3_logs {
      enable = true
    }
    kubernetes {
      audit_logs {
        enable = false
      }
    }
    malware_protection {
      scan_ec2_instance_with_findings {
        ebs_volumes {
          enable = false
        }
      }
    }
  }

  tags = {
    Name    = "SecureWatch GuardDuty"
    Project = "SecureWatch"
  }
}

# =============================================================================
# SNS TOPIC — SECURITY ALERTS MEGAPHONE
# SNS = Simple Notification Service.
# When GuardDuty finds a threat, it publishes to this topic.
# Anything subscribed to this topic gets notified immediately.
# In production this would notify: SIEM, email, PagerDuty, Slack.
# In our project this feeds into the ELK SIEM in Module 5.
# =============================================================================
resource "aws_sns_topic" "security_alerts" {
  name = "${var.project_name}-security-alerts"

  tags = {
    Name    = "SecureWatch Security Alerts"
    Project = "SecureWatch"
  }
}

# =============================================================================
# CLOUDWATCH EVENT RULE — AUTOMATIC ALERT ROUTING
# Think of this as an automatic mail sorter.
# When GuardDuty raises a finding, CloudWatch Events catches it
# and automatically forwards it to SNS without any human involvement.
# This is security automation — a core EMIS requirement.
# =============================================================================
resource "aws_cloudwatch_event_rule" "guardduty_findings" {
  name        = "${var.project_name}-guardduty-findings"
  description = "Route GuardDuty findings to SNS for SIEM ingestion"

  event_pattern = jsonencode({
    source      = ["aws.guardduty"]
    detail-type = ["GuardDuty Finding"]
  })

  tags = {
    Name    = "SecureWatch GuardDuty Events"
    Project = "SecureWatch"
  }
}

resource "aws_cloudwatch_event_target" "guardduty_to_sns" {
  rule      = aws_cloudwatch_event_rule.guardduty_findings.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.security_alerts.arn
}

# Allow CloudWatch Events to publish to SNS
resource "aws_sns_topic_policy" "security_alerts" {
  arn = aws_sns_topic.security_alerts.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudWatchEvents"
        Effect = "Allow"
        Principal = {
          Service = "events.amazonaws.com"
        }
        Action   = "SNS:Publish"
        Resource = aws_sns_topic.security_alerts.arn
      }
    ]
  })
}

# =============================================================================
# SIMULATE SUSPICIOUS ACTIVITY — FOR SIEM DEMONSTRATION
# We create an IAM policy that would be considered overly permissive.
# This gives GuardDuty and our SIEM something real to flag.
# In a real environment this kind of policy would trigger alerts.
# =============================================================================
resource "aws_iam_policy" "overly_permissive_demo" {
  name        = "securewatch-demo-overly-permissive"
  description = "DEMO ONLY: Intentionally overly permissive policy to demonstrate GuardDuty detection"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "DemoOverlyPermissive"
        Effect   = "Allow"
        Action   = "s3:*"
        Resource = "*"
      }
    ]
  })

  tags = {
    Name    = "DEMO-DO-NOT-USE-IN-PRODUCTION"
    Project = "SecureWatch"
  }
}