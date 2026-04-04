import json
import sys

try:
    with open('semgrep-report.json') as f:
        data = json.load(f)
    results = data.get('results', [])
    if not results:
        print('No issues found')
    else:
        print(f'ALERT: {len(results)} vulnerability/vulnerabilities found!')
        for r in results:
            severity = r['extra']['severity']
            check_id = r['check_id']
            path = r['path']
            line = r['start']['line']
            message = r['extra']['message'][:100]
            print(f'  - [{severity}] {check_id}')
            print(f'    File: {path} Line: {line}')
            print(f'    Message: {message}')
            print()
except Exception as e:
    print(f'Could not read report: {e}')
    sys.exit(0)
