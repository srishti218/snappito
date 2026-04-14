import sys
import json
import requests

try:
    res = requests.get('http://localhost:5000/api/services')
    data = res.json()
    for cat in data['categories']:
        for s in cat['services']:
            print(f"{s['service_id']} | {s['name']} | {s['base_price']}")
except Exception as e:
    print(e)
