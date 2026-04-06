# CV Bullet Points — Tailored for EMIS Security Engineer Role

## How to use this document
These bullet points are written using EMIS's exact terminology from their 
job description. Use them to update your CV before applying.
Each bullet uses the format: ACTION + TOOL/TECHNOLOGY + OUTCOME/IMPACT

---

## Projects Section

### SecureWatch Platform — DevSecOps Security Engineering Project
*(Add this as your most recent and prominent project)*

**Azure DevOps & Pipeline Security (directly addresses EMIS's #1 requirement)**
- Designed and implemented a 4-stage Azure DevOps security pipeline integrating 
  Gitleaks secret scanning, Semgrep SAST, and Trivy SCA — automatically blocking 
  vulnerable code from deployment via enforced security quality gates
- Configured a self-hosted Azure Pipelines agent on ARM64 architecture, resolving 
  platform compatibility issues and achieving full pipeline execution across all 
  security scanning stages
- Embedded security controls directly into the CI/CD pipeline for a deliberately 
  vulnerable healthcare application, detecting 5 hardcoded secrets, 12 code 
  vulnerabilities, and 8 CVEs in a single automated scan

**ELK SIEM (marked ESSENTIAL in EMIS JD)**
- Architected and deployed a production-grade ELK SIEM stack (Elasticsearch 8.11, 
  Logstash, Kibana) using Docker, ingesting AWS CloudTrail audit logs and 
  application security events
- Developed Logstash pipeline with custom filter rules mapping detected attacks 
  to MITRE ATT&CK framework techniques including T1190, T1083, T1059, and T1552
- Built a "MediCare Security Operations Centre" Kibana dashboard surfacing 
  real-time threat intelligence across 5 visualizations covering severity 
  breakdown, attack timelines, and MITRE technique distribution

**AWS Security Configuration**
- Provisioned AWS security infrastructure using Terraform IaC including CloudTrail 
  multi-region audit trail, GuardDuty threat detection, encrypted S3 log storage, 
  and SNS/CloudWatch automated alert routing — all tagged with NHS DSP Toolkit 
  and GDPR Article 32 compliance metadata
- Implemented least-privilege IAM user for Terraform with programmatic-only 
  access, demonstrating secure cloud credential management practices
- Enabled CloudTrail log file validation and S3 versioning to ensure audit log 
  integrity and tamper detection — aligned with NHS DSP Toolkit Standard 9

**Vulnerability Testing & Security Assessment**
- Conducted comprehensive vulnerability assessment of a healthcare web application 
  identifying 8 critical/high severity vulnerabilities including SQL injection, 
  command injection, path traversal, and sensitive data exposure
- Produced formal vulnerability assessment report with CVSS scoring, OWASP Top 10 
  mapping, proof-of-concept evidence, and prioritised remediation roadmap
- Demonstrated dynamic security testing by manually exploiting SQL injection to 
  achieve authentication bypass and command injection to achieve remote code 
  execution — providing before/after evidence for all findings

**Threat Modelling**
- Performed STRIDE threat modelling against the MediCare Portal identifying 
  18 discrete threats across all 6 STRIDE categories with MITRE ATT&CK mapping, 
  risk scoring, and recommended security controls
- Produced risk register with inherent and residual risk scoring aligned to 
  NHS DSP Toolkit standards and ISO 27001 risk management methodology

**Security Documentation & IS Policy**
- Authored a suite of 5 security documents including: Vulnerability Assessment 
  Report, STRIDE Threat Model, Information Security Risk Register, IS Security 
  Policy, and Incident Response Runbook — all aligned to NHS DSP Toolkit, 
  GDPR Article 32, and ISO 27001
- Produced GDPR breach notification decision tree and incident response runbooks 
  for SQL injection, credential exposure, and GuardDuty finding scenarios — 
  covering detection, containment, eradication, recovery, and lessons learned

**Scripting & Security Automation**
- Developed Python scripts for Elasticsearch log ingestion, SIEM data parsing, 
  and pipeline reporting — integrating with Azure DevOps artifact publishing
- Wrote Bash scripts for security tool installation, pipeline automation, and 
  infrastructure validation across macOS ARM64 and Linux environments
- Automated end-to-end security scanning using Terraform, Azure DevOps YAML 
  pipelines, and Docker Compose — eliminating manual security checks from 
  the deployment process

---

## Key Skills Section Updates

Add these to your skills section:

**Cloud Platforms:** AWS (CloudTrail, GuardDuty, S3, IAM, SNS, CloudWatch), 
Azure (DevOps, Repos, Pipelines)

**SIEM & Security Tooling:** ELK Stack (Elasticsearch, Logstash, Kibana), 
Gitleaks, Semgrep, Trivy, OWASP ZAP

**Security Practices:** STRIDE Threat Modelling, CVSS Scoring, OWASP Top 10, 
MITRE ATT&CK Framework, GDPR Article 32, NHS DSP Toolkit, ISO 27001

**DevSecOps Tools:** Azure DevOps, Terraform, Docker, Git, GitHub Actions

**Scripting:** Python, Bash, YAML, HCL (Terraform)

---

## Certifications to highlight (you already have these)
- CompTIA Security+
- AWS Certified Cloud Practitioner  
- HashiCorp Certified: Terraform Associate
- Google Cybersecurity Certificate