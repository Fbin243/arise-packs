# Periodic data report

A cron job starts a pipeline every morning. A file-declared action written in Python fetches the totals of each region, an LLM agent summarises them and the summary is emailed.

| Piece                                           | Role                                                                                                   |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `cron/daily-report.yaml`                        | `daily at 07:30`, `then: pipeline.start` with the regions as facts.                                    |
| `actions/report.fetch.yaml` + `report-fetch.py` | A file action: JSON Schema for `with` and `outputs`, `parallelSafe`.                                   |
| `pipelines/sales-report.yaml`                   | `map` runs the action once per region, at most two at a time; then `agent` summarises; `channel.send`. |
| `agents/analyst.yaml`                           | `runtime: llm`.                                                                                        |
| `channels/email.yaml` + `email-send.py`         | Sends the message through an HTTP mail API.                                                            |

Set `REPORT_API_URL`, `EMAIL_API_URL`, `EMAIL_API_KEY`, `REPORT_RECIPIENTS` (comma separated) and `OPENAI_API_KEY` in `~/.arise/.env`; the LLM provider itself (`llm.providers`) stays in your own `config.yaml`.

Install: `arise pack add github:Fbin243/arise-packs/data-report@v1.0.0`. Pack config `subjectPrefix` is put in front of the email subject (the script reads `ARISE_PACK_CONFIG`). Tests: `arise pack test` runs `tests/daily-report.yaml`; the workspace test `tests/packs-data-report.test.ts` installs the pack from a local git remote and runs three scheduled runs.
