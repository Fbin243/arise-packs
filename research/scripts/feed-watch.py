#!/usr/bin/env python3
import json
import sys
import urllib.request

request = json.load(sys.stdin)
url = request["params"]["url"]
seen = set((request.get("state") or {}).get("seen", []))
with urllib.request.urlopen(url, timeout=15) as response:
    items = json.load(response)["items"]
fresh = [item for item in items if item["id"] not in seen]
events = []
if fresh:
    events.append(
        {
            "name": "custom.research.topics",
            "payload": {"topics": [item["title"] for item in fresh], "count": len(fresh)},
            "key": ",".join(item["id"] for item in fresh),
        }
    )
print(json.dumps({"events": events, "state": {"seen": sorted(seen | {item["id"] for item in items})}}))
