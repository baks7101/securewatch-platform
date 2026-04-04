import json
import sys
import os

print('=' * 60)
print('SECUREWATCH SECURITY GATE REPORT')
print('=' * 60)

workspace = os.environ.get('PIPELINE_WORKSPACE', '.')

# Check secrets
try:
    path = os.path.join(workspace, 'secret-scan-results', 'gitleaks-report.json')
    with open(path) as f:
        secrets = json.load(f)
    print(f'Secrets found:        {len(secrets)} issue(s)')
except Exception as e:
    print(f'Secrets found:        Could not read report: {e}')

# Check SAST
try:
    path = os.path.join(workspace, 'sast-results', 'semgrep-report.json')
    with open(path) as f:
        sast = json.load(f)
    print(f'Code vulnerabilities: {len(sast.get("results", []))} issue(s)')
except Exception as e:
    print(f'Code vulnerabilities: Could not read report: {e}')

# Check dependencies
try:
    path = os.path.join(workspace, 'dependency-scan-results', 'trivy-report.json')
    with open(path) as f:
        deps = json.load(f)
    total_cves = sum(len(r.get('Vulnerabilities') or []) for r in deps.get('Results', []))
    print(f'Dependency CVEs:      {total_cves} issue(s)')
except Exception as e:
    print(f'Dependency CVEs:      Could not read report: {e}')

print('=' * 60)
print('STATUS: Pipeline complete. Review findings above.')
print('In production: critical findings would block deployment.')
print('=' * 60)