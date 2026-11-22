#!/usr/bin/env python3
import json
import os
import sys
import urllib.request

event = json.load(sys.stdin)["event"]
config = json.loads(os.environ.get("ARISE_PACK_CONFIG", "{}"))
text = (config.get("mention", "") + " " + event["text"]).strip() if event["actions"] else event["text"]
blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]
if event["actions"]:
    buttons = [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": choice.title()},
            "action_id": choice,
            "value": json.dumps({"kind": "decide", "choice": choice, "quest": event["questId"]}),
        }
        for choice in event["actions"]
    ]
    blocks.append({"type": "actions", "elements": buttons})
body = {"channel": os.environ["SLACK_CHANNEL"], "text": text, "blocks": blocks}
request = urllib.request.Request(
    os.environ["SLACK_API_URL"] + "/chat.postMessage",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + os.environ["SLACK_BOT_TOKEN"]},
)
reply = json.load(urllib.request.urlopen(request, timeout=15))
if not reply.get("ok"):
    sys.exit("slack rejected the message: " + str(reply.get("error")))
