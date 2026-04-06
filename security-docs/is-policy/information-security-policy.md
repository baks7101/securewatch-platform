# Information Security Policy
## SecureWatch Platform

---

| Field | Detail |
|---|---|
| **Document Reference** | SW-POL-2024-001 |
| **Version** | 1.0 |
| **Date** | January 2024 |
| **Author** | Bakary Sillah, Security Engineer |
| **Review Cycle** | Annual |
| **Classification** | Internal |
| **Compliance** | NHS DSP Toolkit, GDPR, ISO 27001 |

---

## 1. Purpose

This Information Security Policy establishes the security requirements for the 
SecureWatch Platform and MediCare Portal. It ensures the confidentiality, integrity, 
and availability of patient data in compliance with:

- UK General Data Protection Regulation (UK GDPR)
- NHS Data Security and Protection Toolkit
- ISO/IEC 27001:2022
- National Cyber Security Centre (NCSC) Cyber Essentials

---

## 2. Scope

This policy applies to:
- All software systems within the SecureWatch Platform
- All personnel with access to patient data
- All third-party suppliers processing patient data
- All cloud infrastructure (AWS eu-west-2, Azure UK South)

---

## 3. Information Security Principles

### 3.1 Confidentiality
Patient identifiable data must only be accessible to authorised clinical staff 
with a legitimate need. Access must be authenticated, authorised, and audited.

### 3.2 Integrity
Patient data must be protected from unauthorised modification. All changes must 
be logged with user, timestamp, and nature of change.

### 3.3 Availability
Clinical systems must maintain 99.9% availability during operational hours. 
Disaster recovery procedures must ensure RTO of 4 hours and RPO of 1 hour.

---

## 4. Access Control Requirements

4.1 All users must authenticate using unique credentials before accessing 
    patient data.

4.2 Multi-factor authentication is mandatory for all administrative accounts 
    and remote access.

4.3 Access must be granted on a least-privilege basis — users receive only 
    the minimum permissions required for their role.

4.4 Privileged accounts (admin, DBA) must be separate from standard user 
    accounts and subject to enhanced monitoring.

4.5 All access to patient data must be logged in the SIEM with user ID, 
    timestamp, and data accessed.

4.6 Access rights must be reviewed quarterly and revoked immediately upon 
    staff departure.

---

## 5. Secure Development Requirements

5.1 All code must undergo SAST scanning before merging to main branch.

5.2 All third-party dependencies must be scanned for known CVEs using SCA 
    tooling (Trivy) on every build.

5.3 Secrets, credentials, and API keys must never be hardcoded in source code. 
    All secrets must be stored in AWS Secrets Manager or Azure Key Vault.

5.4 Security quality gates must be enforced in CI/CD pipelines — critical 
    findings block deployment.

5.5 All SQL queries must use parameterised statements. String concatenation 
    with user input is prohibited.

5.6 Input validation must be applied to all user-supplied data before 
    processing or storing.

5.7 Debug mode must be disabled in all production deployments.

5.8 OWASP Top 10 must be reviewed and addressed during development of all 
    new features.

---

## 6. Cloud Security Requirements

6.1 All cloud resources must be provisioned using Infrastructure as Code 
    (Terraform) and version controlled in a secure repository.

6.2 AWS CloudTrail must be enabled across all regions for all accounts 
    handling patient data.

6.3 Amazon GuardDuty must be enabled and findings must be reviewed within 
    24 hours of generation.

6.4 All S3 buckets containing patient data must have:
    - Public access blocked
    - Encryption at rest (AES-256 minimum)
    - Versioning enabled
    - Access logging enabled

6.5 IAM policies must follow least-privilege. Wildcard (*) permissions 
    are prohibited without documented exception.

6.6 All cloud resources must be tagged with: Project, Environment, 
    Compliance framework, and Data classification.

---

## 7. Security Monitoring Requirements

7.1 A SIEM must be operational and ingesting logs from all systems 
    handling patient data within 30 days of this policy.

7.2 The following events must generate SIEM alerts:
    - Authentication failures (>5 in 10 minutes)
    - Root/admin account usage
    - Privilege escalation attempts
    - Data exfiltration patterns
    - CloudTrail disabled or modified
    - GuardDuty high/critical findings

7.3 SIEM alerts must be triaged within:
    - Critical: 15 minutes
    - High: 1 hour
    - Medium: 4 hours
    - Low: 24 hours

7.4 All security incidents must be documented in the incident register.

---

## 8. Incident Response Requirements

8.1 A documented Incident Response Plan must be maintained and tested 
    annually.

8.2 Personal data breaches must be assessed within 24 hours of discovery.

8.3 Breaches meeting GDPR Article 33 criteria must be reported to the ICO 
    within 72 hours.

8.4 Affected data subjects must be notified without undue delay where 
    there is high risk to their rights and freedoms.

---

## 9. Compliance and Audit

9.1 This policy must be reviewed annually or following significant 
    security incidents.

9.2 Compliance with this policy will be assessed through:
    - Automated pipeline security scanning (continuous)
    - Vulnerability assessments (quarterly)
    - Penetration testing (annual)
    - NHS DSP Toolkit submission (annual)

9.3 Non-compliance must be reported to the Security Engineer and 
    escalated to senior management if not remediated within agreed timescales.

---

## 10. Responsibilities

| Role | Responsibility |
|---|---|
| Security Engineer | Maintain security tools, review findings, update policy |
| Development Teams | Adhere to secure coding standards, remediate findings |
| System Administrators | Apply patches, manage access controls |
| All Staff | Report security incidents, complete security training |
| Data Protection Officer | GDPR compliance, ICO reporting |

---

*Approved by: Bakary Sillah, Security Engineer*
*Version: 1.0 — January 2024*
*Next Review: January 2025*
*Classification: Internal*