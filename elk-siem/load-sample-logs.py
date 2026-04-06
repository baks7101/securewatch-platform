import json
import urllib.request
import base64
import datetime

ES_HOST = "http://localhost:9200"
credentials = base64.b64encode(b"elastic:SecureWatch2024!").decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {credentials}"
}

def send_to_es(index, doc):
    url = f"{ES_HOST}/{index}/_doc"
    data = json.dumps(doc).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"Error: {e}")
        return None

now = datetime.datetime.utcnow()
today = now.strftime("%Y.%m.%d")

def ts(hours_ago=0):
    t = now - datetime.timedelta(hours=hours_ago)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

cloudtrail_events = [
    {"@timestamp": ts(5), "event_name": "ConsoleLogin", "event_source": "iam.amazonaws.com", "source_ip": "185.220.101.45", "aws_region": "eu-west-2", "error_code": "AccessDenied", "user": "root", "userIdentity_type": "Root", "alert_reason": "CRITICAL: Root account used - immediate investigation required", "severity": "CRITICAL", "tags": ["root-usage", "critical", "suspicious"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
    {"@timestamp": ts(5), "event_name": "CreateUser", "event_source": "iam.amazonaws.com", "source_ip": "185.220.101.45", "aws_region": "eu-west-2", "error_code": "AccessDenied", "user": "attacker", "alert_reason": "Sensitive AWS API call detected: CreateUser", "severity": "HIGH", "tags": ["suspicious", "high-priority", "access-denied"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
    {"@timestamp": ts(4), "event_name": "GetSecretValue", "event_source": "secretsmanager.amazonaws.com", "source_ip": "10.0.1.15", "aws_region": "eu-west-2", "secret_id": "medicare-db-password", "alert_reason": "Sensitive AWS API call detected: GetSecretValue", "severity": "HIGH", "tags": ["suspicious", "high-priority"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
    {"@timestamp": ts(4), "event_name": "DeleteTrail", "event_source": "cloudtrail.amazonaws.com", "source_ip": "185.220.101.45", "aws_region": "eu-west-2", "error_code": "AccessDenied", "alert_reason": "Attacker trying to disable audit logging: DeleteTrail", "severity": "CRITICAL", "tags": ["suspicious", "critical", "high-priority"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
    {"@timestamp": ts(3), "event_name": "StopLogging", "event_source": "cloudtrail.amazonaws.com", "source_ip": "185.220.101.45", "aws_region": "eu-west-2", "error_code": "AccessDenied", "alert_reason": "Attacker trying to blind the SIEM: StopLogging", "severity": "CRITICAL", "tags": ["suspicious", "critical", "high-priority"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
    {"@timestamp": ts(3), "event_name": "AttachUserPolicy", "event_source": "iam.amazonaws.com", "source_ip": "185.220.101.45", "aws_region": "eu-west-2", "error_code": "AccessDenied", "alert_reason": "Privilege escalation attempt: AttachUserPolicy", "severity": "HIGH", "tags": ["suspicious", "high-priority"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
    {"@timestamp": ts(2), "event_name": "GetObject", "event_source": "s3.amazonaws.com", "source_ip": "82.34.12.45", "aws_region": "eu-west-2", "alert_reason": "Unusual S3 access pattern detected", "severity": "MEDIUM", "tags": ["suspicious"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "cloudtrail"},
]

medicare_events = [
    {"@timestamp": ts(2), "log_message": "SQL injection attempt: GET /login?username=' OR '1'='1", "source_ip": "192.168.1.100", "endpoint": "/login", "alert_reason": "SQL injection pattern detected", "severity": "HIGH", "mitre_tactic": "T1190 - Exploit Public-Facing Application", "tags": ["sql-injection", "attack-detected"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(2), "log_message": "Path traversal: GET /read-file?filename=../../etc/passwd", "source_ip": "192.168.1.100", "endpoint": "/read-file", "alert_reason": "Path traversal attempt detected", "severity": "HIGH", "mitre_tactic": "T1083 - File and Directory Discovery", "tags": ["path-traversal", "attack-detected"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(1), "log_message": "Command injection: GET /ping?host=localhost;cat /etc/passwd", "source_ip": "192.168.1.100", "endpoint": "/ping", "alert_reason": "Command injection pattern detected", "severity": "CRITICAL", "mitre_tactic": "T1059 - Command and Scripting Interpreter", "tags": ["command-injection", "attack-detected"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(1), "log_message": "Unauthenticated access to patient records: GET /patients", "source_ip": "192.168.1.100", "endpoint": "/patients", "alert_reason": "Sensitive patient data exposed without authentication", "severity": "CRITICAL", "mitre_tactic": "T1530 - Data from Cloud Storage", "tags": ["data-exposure", "attack-detected", "critical"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(1), "log_message": "Brute force: 15 failed logins in 60 seconds", "source_ip": "192.168.1.100", "endpoint": "/login", "alert_reason": "Brute force attack detected", "severity": "HIGH", "mitre_tactic": "T1110 - Brute Force", "tags": ["brute-force", "attack-detected"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(1), "log_message": "Hardcoded AWS credentials in app.py: AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE", "source_ip": "internal", "endpoint": "static-analysis", "alert_reason": "Hardcoded cloud credentials in source code", "severity": "CRITICAL", "mitre_tactic": "T1552 - Unsecured Credentials", "tags": ["hardcoded-secrets", "attack-detected", "critical"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(0), "log_message": "Insecure YAML deserialisation: POST /import-config", "source_ip": "192.168.1.100", "endpoint": "/import-config", "alert_reason": "Insecure deserialisation - possible RCE", "severity": "CRITICAL", "mitre_tactic": "T1190 - Exploit Public-Facing Application", "tags": ["insecure-deserialisation", "attack-detected", "critical"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
    {"@timestamp": ts(0), "log_message": "SQL UNION injection: GET /patient?id=1 UNION SELECT username,password FROM users", "source_ip": "192.168.1.100", "endpoint": "/patient", "alert_reason": "SQL UNION injection - database dump attempt", "severity": "CRITICAL", "mitre_tactic": "T1190 - Exploit Public-Facing Application", "tags": ["sql-injection", "attack-detected", "critical"], "project": "SecureWatch", "compliance": "NHS-DSP-Toolkit", "log_type": "medicare-app"},
]

cloudtrail_index = f"securewatch-cloudtrail-{today}"
medicare_index = f"securewatch-medicare-{today}"

print("Loading CloudTrail events...")
for i, event in enumerate(cloudtrail_events):
    result = send_to_es(cloudtrail_index, event)
    if result:
        print(f"  CloudTrail {i+1}/{len(cloudtrail_events)}: {event['event_name']}")

print("\nLoading MediCare attack events...")
for i, event in enumerate(medicare_events):
    result = send_to_es(medicare_index, event)
    if result:
        print(f"  MediCare {i+1}/{len(medicare_events)}: {event['endpoint']}")

print(f"\nDone! {len(cloudtrail_events) + len(medicare_events)} events loaded")
print(f"Indices: {cloudtrail_index} | {medicare_index}")
