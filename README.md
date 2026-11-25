# arise sample packs

One git repository, four packs, installed the same way as any pack from GitHub. Each directory has an `arise-pack.yaml`, its entries, a README and `tests/` scenarios for `arise pack test`.

| Pack                            | Install source                                     |
| ------------------------------- | -------------------------------------------------- |
| `arise-examples/support-triage` | `github:Fbin243/arise-packs/support-triage@v1.0.2` |
| `arise-examples/data-report`    | `github:Fbin243/arise-packs/data-report@v1.0.2`    |
| `arise-examples/research`       | `github:Fbin243/arise-packs/research@v1.0.2`       |
| `arise-examples/general`        | `github:Fbin243/arise-packs/general@v1.0.2`        |

The four packs are version `1.0.2` in lockstep, so the repository tag `v1.0.2` (created by `arise pack publish`) addresses all of them. Their compatibility range is `arise: ">=1.0 <2"`.

## Install

```sh
arise pack add github:Fbin243/arise-packs/support-triage@v1.0.2
arise pack add github:Fbin243/arise-packs/data-report@v1.0.2
arise pack add github:Fbin243/arise-packs/research@v1.0.2
arise pack add github:Fbin243/arise-packs/general@v1.0.2
```

Set `model: provider/model` in user or project `config.yaml` for agents without a file model, including `general` and the builtin agents. A config `agents.<id>.model` override takes precedence over the agent file, which takes precedence over `model`.

`arise pack add` shows each pack's scripts, permissions, secrets and binaries and asks for confirmation before it activates anything. Set the secrets listed in each pack's README, then the pipelines and triggers are available under the pack's namespace and by short name when unambiguous.

Local equivalents that need no GitHub account: `arise pack add ./support-triage`, or `arise pack add git+file:///path/to/this/repo@v1.0.2#support-triage`.

## Publish a new version

Copy all four pack directories from this repository into the root of a checkout of `Fbin243/arise-packs`, along with this README. A daemon must be running for validate, test and publish; configure its default model first. From that checkout:

```sh
arise pack validate support-triage
arise pack validate data-report
arise pack validate research
arise pack validate general
arise pack test support-triage
arise pack test data-report
arise pack test research
arise pack test general
git add -A
git commit -m "feat(packs): release sample packs 1.0.2"
arise pack publish support-triage
git push origin main v1.0.2
```

`arise pack publish support-triage` validates that pack and creates one repository-wide `v1.0.2` tag that addresses all four packs; do not run publish once per pack with the same tag. In a fresh arise home, install each GitHub source above and check `arise pack list` and `arise doctor`.
