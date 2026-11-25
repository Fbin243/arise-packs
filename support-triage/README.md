# Support ticket triage

A helpdesk webhook starts a repo-less pipeline that classifies the ticket with an LLM, replies on its own to routine tickets and asks a human on Slack before replying to high priority ones.

| Piece                                           | Role                                                                                                                    |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `webhooks/helpdesk.yaml` + `helpdesk-parser.py` | Verifies the HMAC signature and turns a `ticket.created` payload into `custom.helpdesk.ticket.created`.                 |
| `triggers/ticket-created.yaml`                  | `if` skips spam, `dedupeKey` starts one quest per ticket, `then` runs `pipeline.start`.                                 |
| `guardrails/mask-pii.yaml` + `mask-pii.py`      | `beforeAgent` modifies the prompt to mask email addresses and phone numbers, attached to `triager` by its full pack id. |
| `agents/triager.yaml`                           | `runtime: llm`; the `classify` step declares `outputs`, so the answer is a typed object.                                |
| `pipelines/ticket-triage.yaml`                  | `when` branches on `steps.classify.outputs.priority`; `approval` waits for a human.                                     |
| `channels/slack.yaml` + `slack-send.py`         | Posts the message. Approval requests carry Approve and Reject buttons.                                                  |

Each button's `value` is a complete `decide` signal (`{"kind":"decide","choice":"approve","quest":"<id>"}`). Point the Slack interactivity request at a small relay that posts that value to `POST /api/quests/<id>/signal` on the daemon.

Set `HELPDESK_WEBHOOK_SECRET`, `SLACK_API_URL`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL` and `OPENAI_API_KEY` in `~/.arise/.env`.

Install: `arise pack add github:Fbin243/arise-packs/support-triage@v1.0.2`. Pack config `mention` is put in front of approval requests. The exported `mask-pii` guardrail runs from the installed pack before the agent receives its prompt; ticket facts remain unchanged. There is no masking pipeline step or action. Tests: `arise pack test` runs `tests/*.yaml`; `tests/packs-support-triage.test.ts` installs from a temporary local git remote, observes the real `beforeAgent` script returning `modify`, and asserts the fake runtime receives the masked prompt.
