# Information Security Risk Register
## SecureWatch Platform — MediCare Portal

---

| Field | Detail |
|---|---|
| **Document Reference** | SW-RR-2024-001 |
| **Date** | January 2024 |
| **Owner** | Bakary Sillah, Security Engineer |
| **Review Cycle** | Quarterly |
| **Compliance** | NHS DSP Toolkit, GDPR Article 32, ISO 27001 |

---

## Risk Scoring Matrix

**Likelihood:** 1 (Rare) → 5 (Almost Certain)
**Impact:** 1 (Negligible) → 5 (Catastrophic)
**Risk Score:** Likelihood × Impact

| Score | Rating |
|---|---|
| 1-4 | Low |
| 5-9 | Medium |
| 10-14 | High |
| 15-25 | Critical |

---

## Risk Register

### RISK-001: Unauthorised Access to Patient Data
| Field | Detail |
|---|---|
| **Risk ID** | RISK-001 |
| **Category** | Confidentiality |
| **Description** | Patient records accessible without authentication via /patients endpoint |
| **Threat Source** | External attacker, malicious insider |
| **Likelihood (Inherent)** | 5 — Almost Certain |
| **Impact (Inherent)** | 5 — Catastrophic |
| **Inherent Risk Score** | 25 — CRITICAL |
| **Current Controls** | None |
| **Additional Controls Required** | Authentication middleware, RBAC, session management |
| **Likelihood (Residual)** | 1 — Rare |
| **Impact (Residual)** | 2 — Minor |
| **Residual Risk Score** | 2 — LOW |
| **NHS DSP Toolkit** | Standard 7 — Personal Confidential Data |
| **GDPR Article** | Article 5(1)(f), Article 32 |
| **Risk Owner** | Security Engineer |
| **Target Date** | Immediate |

---

### RISK-002: Patient Data Breach via SQL Injection
| Field | Detail |
|---|---|
| **Risk ID** | RISK-002 |
| **Category** | Confidentiality, Integrity |
| **Description** | SQL injection allows authentication bypass and data exfiltration |
| **Threat Source** | External attacker |
| **Likelihood (Inherent)** | 5 — Almost Certain |
| **Impact (Inherent)** | 5 — Catastrophic |
| **Inherent Risk Score** | 25 — CRITICAL |
| **Current Controls** | None |
| **Additional Controls Required** | Parameterised queries, WAF, input validation |
| **Likelihood (Residual)** | 1 — Rare |
| **Impact (Residual)** | 1 — Negligible |
| **Residual Risk Score** | 1 — LOW |
| **NHS DSP Toolkit** | Standard 7, Standard 9 |
| **GDPR Article** | Article 32 |
| **Risk Owner** | Security Engineer |
| **Target Date** | Immediate |

---

### RISK-003: Cloud Credential Compromise
| Field | Detail |
|---|---|
| **Risk ID** | RISK-003 |
| **Category** | Confidentiality, Availability |
| **Description** | AWS credentials hardcoded in source code — exposure leads to full cloud account compromise |
| **Threat Source** | External attacker, code repository breach |
| **Likelihood (Inherent)** | 4 — Likely |
| **Impact (Inherent)** | 5 — Catastrophic |
| **Inherent Risk Score** | 20 — CRITICAL |
| **Current Controls** | None |
| **Additional Controls Required** | AWS Secrets Manager, credential rotation, Gitleaks scanning |
| **Likelihood (Residual)** | 1 — Rare |
| **Impact (Residual)** | 2 — Minor |
| **Residual Risk Score** | 2 — LOW |
| **NHS DSP Toolkit** | Standard 9 — Cyber Security |
| **GDPR Article** | Article 32 |
| **Risk Owner** | Security Engineer |
| **Target Date** | Immediate |

---

### RISK-004: Remote Code Execution via Command Injection
| Field | Detail |
|---|---|
| **Risk ID** | RISK-004 |
| **Category** | Integrity, Availability |
| **Description** | Command injection in /ping endpoint allows arbitrary OS command execution |
| **Threat Source** | External attacker |
| **Likelihood (Inherent)** | 4 — Likely |
| **Impact (Inherent)** | 5 — Catastrophic |
| **Inherent Risk Score** | 20 — CRITICAL |
| **Current Controls** | None |
| **Additional Controls Required** | Input validation, remove shell=True, WAF |
| **Likelihood (Residual)** | 1 — Rare |
| **Impact (Residual)** | 1 — Negligible |
| **Residual Risk Score** | 1 — LOW |
| **NHS DSP Toolkit** | Standard 9 |
| **GDPR Article** | Article 32 |
| **Risk Owner** | Security Engineer |
| **Target Date** | Immediate |

---

### RISK-005: Regulatory Non-Compliance — GDPR Breach Notification
| Field | Detail |
|---|---|
| **Risk ID** | RISK-005 |
| **Category** | Compliance |
| **Description** | Multiple vulnerabilities constitute personal data breaches requiring ICO notification within 72 hours |
| **Threat Source** | Regulatory |
| **Likelihood (Inherent)** | 5 — Almost Certain |
| **Impact (Inherent)** | 4 — Major |
| **Inherent Risk Score** | 20 — CRITICAL |
| **Current Controls** | None |
| **Additional Controls Required** | Incident response plan, breach notification procedure, DPO engagement |
| **Likelihood (Residual)** | 2 — Unlikely |
| **Impact (Residual)** | 2 — Minor |
| **Residual Risk Score** | 4 — LOW |
| **NHS DSP Toolkit** | Standard 1 — Personal Confidential Data Policy |
| **GDPR Article** | Article 33 — Notification of Breach |
| **Risk Owner** | Data Protection Officer |
| **Target Date** | Immediate |

---

## Risk Summary

| Risk ID | Description | Inherent | Residual | Status |
|---|---|---|---|---|
| RISK-001 | Unauthorised patient data access | CRITICAL (25) | LOW (2) | Open |
| RISK-002 | SQL injection data breach | CRITICAL (25) | LOW (1) | Open |
| RISK-003 | Cloud credential compromise | CRITICAL (20) | LOW (2) | Open |
| RISK-004 | Remote code execution | CRITICAL (20) | LOW (1) | Open |
| RISK-005 | GDPR non-compliance | CRITICAL (20) | LOW (4) | Open |

---

*Document Owner: Bakary Sillah, Security Engineer*
*Next Review: April 2024*
*Classification: CONFIDENTIAL*