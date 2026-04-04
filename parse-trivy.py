import json
import sys

try:
    with open('trivy-report.json') as f:
        data = json.load(f)
    results = data.get('Results', [])
    total = 0
    for result in results:
        vulns = result.get('Vulnerabilities', []) or []
        total += len(vulns)
        for v in vulns:
            severity = v.get('Severity', 'UNKNOWN')
            vuln_id = v.get('VulnerabilityID', 'N/A')
            pkg = v.get('PkgName', 'N/A')
            installed = v.get('InstalledVersion', 'N/A')
            fixed = v.get('FixedVersion', 'no fix available')
            print(f'  - [{severity}] {vuln_id}')
            print(f'    Package: {pkg} {installed}')
            print(f'    Fix: upgrade to {fixed}')
            print()
    print(f'Total CVEs found: {total}')
except Exception as e:
    print(f'Could not read report: {e}')
    sys.exit(0)
