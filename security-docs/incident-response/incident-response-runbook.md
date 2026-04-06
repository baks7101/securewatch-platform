# Incident Response Runbook
## SecureWatch Platform — MediCare Portal

---

| Field | Detail |
|---|---|
| **Document Reference** | SW-IR-2024-001 |
| **Version** | 1.0 |
| **Date** | January 2024 |
| **Author** | Bakary Sillah, Security Engineer |
| **Classification** | CONFIDENTIAL |
| **Compliance** | NHS DSP Toolkit, GDPR Article 33 |

---

## 1. Incident Response Phases
```
DETECT → ANALYSE → CONTAIN → ERADICATE → RECOVER → LESSONS LEARNED
```

---

## 2. Incident Classification

| Severity | Definition | Response Time | Example |
|---|---|---|---|
| P1 — Critical | Active breach of patient data | 15 minutes | SQL injection extracting NHS records |
| P2 — High | Attempted breach, system compromise | 1 hour | Successful command injection |
| P3 — Medium | Suspicious activity, policy violation | 4 hours | Multiple failed logins |
| P4 — Low | Minor policy violation, low risk | 24 hours | Outdated dependency found |

---

## 3. Runbook: SQL Injection Attack Detected

**Trigger:** SIEM alert — SQL injection pattern in application logs
**Severity:** P1 — Critical

### Phase 1 — DETECT (0-15 minutes)
- [ ] SIEM alert received in Kibana dashboard
- [ ] Verify alert is not a false positive — check raw log in Discover
- [ ] Confirm attack source IP and targeted endpoint
- [ ] Check if data was successfully extracted (HTTP 200 response?)
- [ ] Declare incident — notify Security Engineer immediately

### Phase 2 — ANALYSE (15-30 minutes)
- [ ] Pull all logs from source IP for last 24 hours from ELK
- [ ] Identify all endpoints accessed by attacker
- [ ] Determine what data was accessed or exfiltrated
- [ ] Assess whether patient data was compromised
- [ ] Run KQL query in Kibana:
```
source_ip: "[ATTACKER IP]" AND @timestamp >= "now-24h"
```

### Phase 3 — CONTAIN (30-60 minutes)
- [ ] Block attacker IP at WAF/firewall level immediately
- [ ] If AWS involved — revoke compromised IAM credentials
- [ ] Isolate affected application instance if breach confirmed
- [ ] Preserve all logs — do not delete or modify evidence
- [ ] Notify Data Protection Officer if patient data accessed

### Phase 4 — ERADICATE (1-4 hours)
- [ ] Apply parameterised query fix to all SQL injection points
- [ ] Deploy patched application to staging
- [ ] Run full SAST scan on patched code
- [ ] Verify fix eliminates vulnerability with targeted retest
- [ ] Review all similar endpoints for same vulnerability

### Phase 5 — RECOVER (4-8 hours)
- [ ] Deploy patched application to production
- [ ] Verify application functioning correctly
- [ ] Monitor SIEM for 24 hours post-recovery
- [ ] Restore any affected data from backup if needed
- [ ] Confirm attacker no longer has access

### Phase 6 — LESSONS LEARNED (Within 5 days)
- [ ] Document full incident timeline
- [ ] Root cause analysis — why was this vulnerability present?
- [ ] Update secure coding standards
- [ ] Add test case to prevent regression
- [ ] Update risk register
- [ ] Consider GDPR breach notification requirement

---

## 4. Runbook: Hardcoded Credentials Detected

**Trigger:** Gitleaks alert in Azure DevOps pipeline
**Severity:** P1 — Critical

### Phase 1 — DETECT
- [ ] Pipeline alert received — Gitleaks found credentials in commit
- [ ] Identify which credentials were exposed (AWS keys, passwords, API keys)
- [ ] Determine how long credentials have been in repository
- [ ] Check git history — were credentials ever pushed to remote?

### Phase 2 — ANALYSE
- [ ] Check AWS CloudTrail for any usage of exposed access keys
- [ ] Check for unusual API calls, resource creation, data access
- [ ] Determine if credentials were accessed by unauthorised parties
- [ ] Run CloudTrail query in ELK SIEM for exposed key usage

### Phase 3 — CONTAIN
- [ ] Immediately rotate/revoke all exposed credentials
- [ ] In AWS Console: IAM → Users → Security Credentials → Deactivate key
- [ ] Generate new credentials and store in AWS Secrets Manager
- [ ] Remove credentials from git history using git-filter-repo
- [ ] Force push cleaned history to all remotes

### Phase 4 — ERADICATE
- [ ] Update application to use AWS Secrets Manager
- [ ] Add Gitleaks pre-commit hook to prevent future occurrences
- [ ] Add .secrets.baseline file to repository
- [ ] Update pipeline to fail on any secret detection

### Phase 5 — RECOVER
- [ ] Verify application works with new credentials from Secrets Manager
- [ ] Run full pipeline scan to confirm no remaining secrets
- [ ] Monitor CloudTrail for 72 hours for any activity using old credentials

---

## 5. Runbook: GuardDuty High/Critical Finding

**Trigger:** GuardDuty finding routed via SNS to SIEM
**Severity:** P1/P2 depending on finding type

### Phase 1 — DETECT
- [ ] GuardDuty finding appears in ELK SIEM
- [ ] Review finding type and severity in AWS GuardDuty console
- [ ] Common critical finding types:
  - UnauthorizedAccess:IAMUser/MaliciousIPCaller
  - Recon:IAMUser/MaliciousIPCaller
  - CryptoCurrency:EC2/BitcoinTool
  - Exfiltration:S3/MaliciousIPCaller

### Phase 2 — ANALYSE
- [ ] Identify affected AWS resource (EC2 instance, IAM user, S3 bucket)
- [ ] Pull CloudTrail logs for affected resource from last 24 hours
- [ ] Determine scope of potential compromise
- [ ] Check if patient data in S3 was accessed

### Phase 3 — CONTAIN
- [ ] If EC2 compromised: isolate instance (remove from security group)
- [ ] If IAM compromised: disable affected user, rotate all credentials
- [ ] If S3 accessed: review bucket access logs, block public access
- [ ] Preserve GuardDuty finding — do not archive until investigation complete

### Phase 4 — ERADICATE
- [ ] Terminate compromised EC2 instances
- [ ] Delete unauthorised IAM users or access keys
- [ ] Review and tighten IAM policies
- [ ] Patch exploited vulnerabilities

### Phase 5 — RECOVER
- [ ] Rebuild infrastructure from Terraform (clean state)
- [ ] Restore data from verified clean backup
- [ ] Verify GuardDuty shows no new findings
- [ ] Enhanced monitoring for 7 days post-incident

---

## 6. GDPR Breach Notification Decision Tree
```
Patient data accessed by unauthorised party?
├── NO → Internal incident only, document and remediate
└── YES → Is there risk to individuals' rights and freedoms?
    ├── NO → Document, no ICO notification required
    └── YES → Notify ICO within 72 hours (Article 33)
        └── Is risk HIGH to individuals?
            ├── NO → ICO notification only
            └── YES → Notify affected patients (Article 34)
```

**ICO Reporting Portal:** https://ico.org.uk/for-organisations/report-a-breach/

**Information required for ICO notification:**
- Nature of breach and data categories affected
- Approximate number of individuals affected
- Likely consequences of the breach
- Measures taken or proposed to address breach

---

## 7. Key Contacts

| Role | Responsibility |
|---|---|
| Security Engineer | Incident lead, technical response |
| Data Protection Officer | GDPR compliance, ICO notification |
| Senior Management | Business decisions, media response |
| Legal Team | Legal advice, regulatory liaison |
| NHS Digital DSPT Team | NHS-specific guidance |

---

*Document: SW-IR-2024-001*
*Author: Bakary Sillah, Security Engineer*
*Classification: CONFIDENTIAL*