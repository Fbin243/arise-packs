#!/usr/bin/env python3
import json
import re
import sys

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")

request = json.load(sys.stdin)
data = request["input"]
prompt = data.get("prompt", "")
masked = PHONE.sub("[phone]", EMAIL.sub("[email]", prompt))
if masked == prompt:
    print(json.dumps({"decision": "allow"}))
else:
    print(json.dumps({"decision": "modify", "input": {**data, "prompt": masked}}))
