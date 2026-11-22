#!/usr/bin/env python3
import json
import sys

request = json.load(sys.stdin)
payload = request.get("payload") or {}
if payload.get("type") != "ticket.created":
    print("[SILENT]")
    sys.exit(0)
ticket = payload["ticket"]
event = {
    "name": "custom.helpdesk.ticket.created",
    "payload": {
        "id": str(ticket["id"]),
        "subject": ticket.get("subject", ""),
        "body": ticket.get("body", ""),
        "requester": ticket.get("requester", ""),
        "tags": ticket.get("tags", []),
    },
}
print(json.dumps({"events": [event]}))
