import requests
import json
import time

url = "http://127.0.0.1:5000/webhook"
zone_id = "2025-07-17T08:12:00_41230_bullish"

payloads = [
    {
        "timeframe": "4hr",
        "event": "fib_30_touch",
        "zone_id": zone_id,
        "price": 18201.50,
        "bounce_pts": 10,
        "direction": "bullish",
        "parent_structure": "bullish"
    },
    {
        "timeframe": "4hr",
        "event": "fib_50_touch",
        "zone_id": zone_id,
        "price": 18225.75,
        "bounce_pts": 15,
        "direction": "bullish",
        "parent_structure": "bullish"
    },
    {
        "timeframe": "4hr",
        "event": "fib_70_touch",
        "zone_id": zone_id,
        "price": 18240.00,
        "bounce_pts": 20,
        "direction": "bullish",
        "parent_structure": "bullish"
    }
]

headers = {"Content-Type": "application/json"}

for p in payloads:
    response = requests.post(url, data=json.dumps(p), headers=headers)
    print(f"Sent: {p['event']} | Status: {response.status_code} | Response: {response.json()}")
    time.sleep(1)