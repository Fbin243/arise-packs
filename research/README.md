# Multi-agent research

A watcher polls a JSON feed. New items start a research quest that fans out one child quest per topic; when the research quest completes a trigger starts the synthesis pipeline.

| Piece                                                | Role                                                                                                                    |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `watchers/research.feed.yaml` + `feed-watch.py`      | Remembers the ids it has seen in `state`, emits `custom.research.topics` for new ones, `then: pipeline.start research`. |
| `pipelines/research.yaml`                            | `map` over `facts.topics` with `pipeline.call research-topic`; keeps the summaries as facts.                            |
| `pipelines/research-topic.yaml`                      | `researcher` (external ACP agent) then `editor` (llm, typed `outputs`). No repository: agents run in a scratch folder.  |
| `runtimes/research-agent.yaml`                       | Declares the ACP runtime (`command`, `args`, `env`). Install a command called `research-agent` that speaks ACP.         |
| `triggers/synthesize.yaml` + `research-completed.py` | `when: quest.completed`; the filter script reads the quest from the daemon API and stays silent for other pipelines.    |
| `pipelines/synthesis.yaml`                           | One agent combines the summaries and delivers the briefing.                                                             |

Start the watch with `arise watch add research.feed --param url=https://news.example.com/feed.json`. Set `RESEARCH_AGENT_KEY` and `OPENAI_API_KEY` in `~/.arise/.env`; `ARISE_PORT` (or `ARISE_API_URL`) tells the filter script where the daemon listens.

Your own `config.yaml` can bound the researcher with `limits.semaphores.model: { research-agent/deep: 2 }`. Install: `arise pack add github:Fbin243/arise-packs/research@v1.0.0`. Tests: `arise pack test` runs `tests/feed-research.yaml`; the workspace test `tests/packs-research.test.ts` installs the pack from a local git remote with an ACP stand-in behind the declared runtime.
