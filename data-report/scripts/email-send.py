#!/usr/bin/env python3
import json
import os
import sys
import urllib.request

event = json.load(sys.stdin)["event"]
config = json.loads(os.environ.get("ARISE_PACK_CONFIG", "{}"))
subject = config.get("subjectPrefix", "") + event["text"].splitlines()[0][:80]
body = {"to": os.environ["REPORT_RECIPIENTS"].split(","), "subject": subject, "text": event["text"], "kind": event["kind"]}
request = urllib.request.Request(
    os.environ["EMAIL_API_URL"] + "/send",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["EMAIL_API_KEY"]},
)
urllib.request.urlopen(request, timeout=20).read()
