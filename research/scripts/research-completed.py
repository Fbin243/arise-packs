#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
import urllib.request

event = json.load(sys.stdin)["event"]
base = os.environ.get("ARISE_API_URL") or "http://127.0.0.1:" + os.environ.get("ARISE_PORT", "7777")
token = os.environ.get("ARISE_API_TOKEN")
if not token:
    token = (Path(os.environ.get("ARISE_HOME", Path.home() / ".arise")) / "state" / "api-token").read_text().strip()
request = urllib.request.Request(base + "/api/quests/" + event["quest"], headers={"Authorization": "Bearer " + token})
with urllib.request.urlopen(request, timeout=15) as response:
    quest = json.load(response)
summaries = quest["facts"].get("summaries")
if quest["pipeline"] != os.environ["ARISE_PACK_ID"] + ":research" or summaries is None:
    print("[SILENT]")
else:
    print(json.dumps({"payload": {**event, "title": quest["title"], "summaries": summaries}}))
