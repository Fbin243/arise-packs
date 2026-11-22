#!/usr/bin/env python3
import json
import os
import sys
import urllib.parse
import urllib.request

params = json.load(sys.stdin)["params"]
query = urllib.parse.urlencode({"region": params["region"], "days": params.get("days", 1)})
with urllib.request.urlopen(os.environ["REPORT_API_URL"] + "/orders?" + query, timeout=20) as response:
    rows = json.load(response)["rows"]
outputs = {
    "region": params["region"],
    "orders": len(rows),
    "revenue": round(sum(row["amount"] for row in rows), 2),
}
print(json.dumps({"outcome": "success", "detail": f"{outputs['orders']} orders", "outputs": outputs}))
