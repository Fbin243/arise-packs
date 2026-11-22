# arise sample packs

One git repository, three packs, installed the same way as any pack from GitHub. Each directory has an `arise-pack.yaml`, the entries (agents, pipelines, triggers, cron, actions, watchers, webhooks, channels, runtimes), `scripts/`, a README and `tests/` scenarios for `arise pack test`.

| Pack                            | Install source                                     |
| ------------------------------- | -------------------------------------------------- |
| `arise-examples/support-triage` | `github:Fbin243/arise-packs/support-triage@v1.0.0` |
| `arise-examples/data-report`    | `github:Fbin243/arise-packs/data-report@v1.0.0`    |
| `arise-examples/research`       | `github:Fbin243/arise-packs/research@v1.0.0`       |

The three packs are version `1.0.0` in lockstep, so the repository tag `v1.0.0` (created by `arise pack publish`) addresses all of them.

## Install

```sh
arise pack add github:Fbin243/arise-packs/support-triage@v1.0.0
arise pack add github:Fbin243/arise-packs/data-report@v1.0.0
arise pack add github:Fbin243/arise-packs/research@v1.0.0
```

`arise pack add` shows each pack's scripts, permissions, secrets and binaries and asks for confirmation before it activates anything. Set the secrets listed in each pack's README, then the pipelines and triggers are available under the pack's namespace (for example `arise-examples/support-triage:ticket-triage`) and by short name when it is unambiguous.

Local equivalents that need no GitHub account: `arise pack add ./support-triage`, or `arise pack add git+file:///path/to/this/repo@v1.0.0#support-triage`.

## Publish a new version

A daemon must be running for validate, test and publish. Bump `version` in all three manifests together, then:

```sh
arise pack validate support-triage
arise pack validate data-report
arise pack validate research
arise pack test support-triage
arise pack test data-report
arise pack test research
git add -A
git commit -m "feat: release sample packs"
arise pack publish support-triage
git push origin main v<version>
```

`arise pack publish support-triage` validates that pack and creates one repository-wide `v<version>` tag that addresses all three packs; do not run publish once per pack with the same tag.
