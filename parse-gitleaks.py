import json
import sys

try:
    with open('gitleaks-report.json') as f:
        data = json.load(f)
    if not data:
        print('No secrets found')
    else:
        print(f'ALERT: {len(data)} secret(s) detected!')
        for item in data:
            print(f'  - {item["Description"]} in {item["File"]} at line {item["StartLine"]}')
except Exception as e:
    print(f'Could not read report: {e}')
    sys.exit(0)