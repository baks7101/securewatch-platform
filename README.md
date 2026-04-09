# SecureWatch Platform
### End-to-End DevSecOps Security Engineering Portfolio Project

![Azure DevOps](https://img.shields.io/badge/Azure%20DevOps-Pipeline-blue)
![AWS](https://img.shields.io/badge/AWS-CloudTrail%20%7C%20GuardDuty-orange)
![ELK](https://img.shields.io/badge/ELK-SIEM-green)
![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)

---

## Overview

SecureWatch is a comprehensive security engineering portfolio project simulating
a real-world healthcare security environment. It demonstrates end-to-end security
engineering capability across application security, pipeline security, cloud
security, and security operations.

The project uses a deliberately vulnerable healthcare application (MediCare Portal)
as its target, demonstrating the full security engineering lifecycle from vulnerability
discovery through to SIEM detection and formal documentation.

---

## Architecture

## Architecture

![SecureWatch Architecture](https://raw.githubusercontent.com/baks7101/securewatch-platform/master/architecture-diagram.svg)

---

## Modules

### Module 2 — Deliberately Vulnerable Application
A Flask-based healthcare patient portal containing 8 intentional vulnerabilities:

| Vulnerability | CWE | OWASP | Severity |
|---|---|---|---|
| SQL Injection (Authentication) | CWE-89 | A03:2021 | Critical |
| Hardcoded Credentials | CWE-798 | A07:2021 | Critical |
| Sensitive Data Exposure | CWE-306 | A01:2021 | Critical |
| Command Injection | CWE-78 | A03:2021 | Critical |
| Path Traversal | CWE-22 | A01:2021 | High |
| Vulnerable Dependencies | CWE-1035 | A06:2021 | High |
| Insecure Deserialisation | CWE-502 | A08:2021 | High |
| Debug Mode Enabled | CWE-94 | A05:2021 | High |

---

### Module 3 — Azure DevOps Security Pipeline
4-stage automated security pipeline running on every code push:

- **Stage 1:** Gitleaks secret scanning — detected 5 hardcoded secrets
- **Stage 2:** Semgrep SAST — detected 12 code vulnerabilities
- **Stage 3:** Trivy SCA — detected 8 CVEs in dependencies
- **Stage 4:** Security Gate — consolidated report with pass/fail decision

---

### Module 4 — AWS Security Infrastructure (Terraform)
All resources provisioned as Infrastructure as Code:

- **CloudTrail** — multi-region audit trail with log file validation
- **GuardDuty** — ML-based threat detection across all data sources
- **S3** — encrypted, versioned, private log storage
- **SNS + CloudWatch** — automated alert routing pipeline
- **Compliance tagging** — NHS DSP Toolkit and GDPR Article 32

---

### Module 5 — ELK SIEM Stack
Production-grade Security Information and Event Management system:

- **Elasticsearch 8.11** — stores and indexes all security events
- **Logstash** — ingests CloudTrail and application logs with custom parsing rules
- **Kibana** — MediCare Security Operations Centre dashboard
- **MITRE ATT&CK mapping** — all attacks tagged with technique IDs
- **Alert rules** — SQL injection, path traversal, command injection, credential exposure, suspicious AWS API calls

---

### Module 6 — Security Documentation
Professional security documentation suite:

- **Vulnerability Assessment Report** — 8 findings with CVSS scores, PoC evidence, and remediation guidance
- **STRIDE Threat Model** — 18 threats across all categories with MITRE ATT&CK mapping
- **Risk Register** — ISO 27001-aligned with inherent/residual scoring
- **IS Security Policy** — NHS DSP Toolkit and GDPR Article 32 aligned
- **Incident Response Runbook** — SQL injection, credential exposure, and GuardDuty finding playbooks with GDPR breach notification tree

---

## Technologies Used

| Category | Technologies |
|---|---|
| Cloud | AWS (CloudTrail, GuardDuty, S3, IAM, SNS), Azure (DevOps, Repos) |
| SIEM | Elasticsearch, Logstash, Kibana (ELK Stack 8.11) |
| Security Scanning | Gitleaks, Semgrep, Trivy |
| IaC | Terraform, Docker, Docker Compose |
| Languages | Python, Bash, YAML, HCL |
| Frameworks | STRIDE, MITRE ATT&CK, OWASP Top 10, CVSS 3.1 |
| Compliance | NHS DSP Toolkit, GDPR Article 32, ISO 27001 |

---

## Compliance Alignment

| Standard | Coverage |
|---|---|
| NHS DSP Toolkit | Standards 7, 9 — personal data, cyber security |
| GDPR Article 32 | Security of processing controls |
| GDPR Article 33 | Breach notification procedures |
| ISO 27001:2022 | Risk management methodology |
| OWASP Top 10 2021 | All 10 categories addressed |
| MITRE ATT&CK | T1059, T1083, T1190, T1530, T1552 mapped |

---

## Author
**Bakary Sillah** — Security Engineer

CompTIA Security+ | AWS CCP | Terraform Associate

[LinkedIn](https://linkedin.com) | [Email](mailto:bsillah15@gmail.com)