# General work

A single-agent pipeline for research, writing, analysis and small changes that do not need a specialised pipeline.

Install with `arise pack add github:Fbin243/arise-packs/general@v1.0.2`. Set `model: provider/model` in your user or project `config.yaml`; the agent has no hardcoded model or display name. Run `arise quest "Summarise the documentation" --pipeline general`.

To make it available to the builtin router, include `general` in the `pipelines` allowlist under the quest's `route.with` fact. There is no implicit fallback.

Validate and run the fake-agent scenario with `arise pack validate general` and `arise pack test general` from the parent directory.
