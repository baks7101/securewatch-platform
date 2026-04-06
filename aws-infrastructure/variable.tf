variable "aws_region" {
  description = "AWS region — eu-west-2 is London, closest to Bristol and GDPR compliant for UK healthcare data"
  type        = string
  default     = "eu-west-2"
}

variable "project_name" {
  description = "Project name used as prefix for all resource names"
  type        = string
  default     = "securewatch"
}

variable "environment" {
  description = "Environment name for tagging"
  type        = string
  default     = "dev"
}