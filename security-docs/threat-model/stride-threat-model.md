# STRIDE Threat Model
## MediCare Patient Portal — SecureWatch Platform

---

| Field | Detail |
|---|---|
| **Document Reference** | SW-TM-2024-001 |
| **Date** | January 2024 |
| **Author** | Bakary Sillah, Security Engineer |
| **Framework** | STRIDE + MITRE ATT&CK |
| **Compliance** | NHS DSP Toolkit, GDPR Article 32 |

---

## 1. System Overview

The MediCare Portal is a Flask-based web application that allows clinical staff 
to access, search, and manage patient records. It connects to a SQLite database 
containing patient identifiable information (PII) including NHS numbers, 
diagnoses, and dates of birth.

### Data Flow Diagram
```
[Clinical Staff] → [MediCare Portal] → [SQLite Database]
                         ↓
                   [AWS S3 Bucket]
                         ↓
                   [ELK SIEM]
```

---

## 2. STRIDE Analysis

STRIDE is a threat modelling framework developed by Microsoft. Each letter 
represents a category of threat:

| Letter | Threat | Question it asks |
|---|---|---|
| S | Spoofing | Can an attacker pretend to be someone else? |
| T | Tampering | Can an attacker modify data? |
| R | Repudiation | Can an attacker deny doing something? |
| I | Information Disclosure | Can an attacker read data they shouldn't? |
| D | Denial of Service | Can an attacker make the system unavailable? |
| E | Elevation of Privilege | Can an attacker gain more access than allowed? |

---

### S — Spoofing Threats

| ID | Threat | Component | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| S-01 | Attacker bypasses login using SQL injection | /login endpoint | HIGH | CRITICAL | CRITICAL |
| S-02 | Attacker uses stolen credentials from hardcoded secrets | app.py | HIGH | CRITICAL | CRITICAL |
| S-03 | Session token forgery due to weak SECRET_KEY | Flask session | MEDIUM | HIGH | HIGH |

**Mitigations:**
- Implement parameterised queries (eliminates S-01)
- Move credentials to AWS Secrets Manager (eliminates S-02)
- Generate SECRET_KEY from cryptographically secure source (mitigates S-03)
- Implement MFA for clinical staff accounts

---

### T — Tampering Threats

| ID | Threat | Component | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| T-01 | Attacker modifies patient records via SQL injection | /patient endpoint | HIGH | CRITICAL | CRITICAL |
| T-02 | Attacker uploads malicious YAML config | /import-config | MEDIUM | CRITICAL | HIGH |
| T-03 | Attacker modifies CloudTrail logs to cover tracks | AWS S3 | LOW | HIGH | MEDIUM |

**Mitigations:**
- Parameterised queries prevent SQL tampering (T-01)
- yaml.safe_load() prevents YAML code execution (T-02)
- CloudTrail log file validation enabled — tampering detected (T-03)
- S3 versioning enabled — deleted logs recoverable

---

### R — Repudiation Threats

| ID | Threat | Component | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| R-01 | No audit log of who accessed patient records | Application | HIGH | HIGH | HIGH |
| R-02 | Attacker disables CloudTrail to hide activity | AWS | LOW | CRITICAL | HIGH |
| R-03 | Debug logs expose sensitive queries | app.py | HIGH | MEDIUM | MEDIUM |

**Mitigations:**
- Implement application-level audit logging for all patient data access
- CloudTrail multi-region trail with log validation prevents R-02
- Remove debug logging of SQL queries (R-03)
- ELK SIEM provides immutable audit trail

---

### I — Information Disclosure Threats

| ID | Threat | Component | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| I-01 | Patient records exposed without authentication | /patients | CRITICAL | CRITICAL | CRITICAL |
| I-02 | Server files readable via path traversal | /read-file | HIGH | HIGH | HIGH |
| I-03 | Database errors expose schema information | All endpoints | HIGH | MEDIUM | MEDIUM |
| I-04 | AWS credentials exposed in source code | app.py | CRITICAL | CRITICAL | CRITICAL |

**MITRE ATT&CK Mapping:**
- I-01 → T1530: Data from Cloud Storage Object
- I-02 → T1083: File and Directory Discovery
- I-04 → T1552: Unsecured Credentials

**Mitigations:**
- Require authentication on all patient data endpoints (I-01)
- Implement path validation with allowed directory list (I-02)
- Generic error messages only — no stack traces in production (I-03)
- AWS Secrets Manager for all credentials (I-04)

---

### D — Denial of Service Threats

| ID | Threat | Component | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| D-01 | Resource exhaustion via repeated SQL injection attempts | Database | MEDIUM | HIGH | HIGH |
| D-02 | Command injection used to consume server resources | /ping | HIGH | HIGH | HIGH |
| D-03 | Debug mode exposes Werkzeug debugger — can crash server | Flask | MEDIUM | HIGH | MEDIUM |

**Mitigations:**
- Rate limiting on all endpoints
- Disable debug mode in production
- AWS WAF rate-based rules
- Input validation on all parameters

---

### E — Elevation of Privilege Threats

| ID | Threat | Component | Likelihood | Impact | Risk |
|---|---|---|---|---|---|
| E-01 | SQL injection retrieves admin credentials | /login | HIGH | CRITICAL | CRITICAL |
| E-02 | Command injection runs commands as root | /ping | HIGH | CRITICAL | CRITICAL |
| E-03 | Overly permissive IAM policy allows S3 full access | AWS IAM | HIGH | HIGH | HIGH |

**MITRE ATT&CK Mapping:**
- E-01 → T1078: Valid Accounts
- E-02 → T1068: Exploitation for Privilege Escalation
- E-03 → T1078.004: Cloud Accounts

**Mitigations:**
- Parameterised queries prevent credential theft via SQL (E-01)
- Remove shell=True from all subprocess calls (E-02)
- Implement least-privilege IAM policies (E-03)

---

## 3. Risk Heat Map
```
         IMPACT
         Low    Medium    High    Critical
L  High  |      | R-03   | D-01  | S-03
I        |      |        | T-03  |
K Medium |      |        | D-03  | T-02
E        |      |        | R-02  |
L  Low   |      |        |       | T-01,S-01
I        |      |        |       | S-02,I-01
H        |      |        |       | I-04,E-01
O        |      |        |       | E-02
O
D
```

---

## 4. Recommended Security Controls

| Control | Type | Priority | Maps To |
|---|---|---|---|
| Parameterised queries | Preventive | P1 | S-01, T-01, E-01 |
| AWS Secrets Manager | Preventive | P1 | S-02, I-04 |
| Authentication middleware | Preventive | P1 | I-01 |
| Input validation | Preventive | P1 | I-02, D-02 |
| WAF deployment | Detective/Preventive | P2 | D-01, D-02 |
| Rate limiting | Preventive | P2 | D-01 |
| Audit logging | Detective | P2 | R-01 |
| SIEM alerting | Detective | P2 | All |
| Least privilege IAM | Preventive | P2 | E-03 |

---

*Document prepared by: Bakary Sillah, Security Engineer*
*Framework: STRIDE (Microsoft) + MITRE ATT&CK*
*Compliance: NHS DSP Toolkit Standard 7, GDPR Article 32*