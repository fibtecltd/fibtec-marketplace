# Fibtec marketplace

A [Claude Code](https://code.claude.com) plugin marketplace for the products of [Fibtec Limited](https://www.fibtec.co.uk):
pyvar (risk computation), ETL Integrator and TenGrade. It is a **catalogue only**: each plugin lives, is versioned and is
released in its own repository, and this repository just lists where.

## Add it

In Claude Code:

```
/plugin marketplace add fibtecltd/fibtec-marketplace
/plugin install pyvar-mcp@fibtec-marketplace
```

or from a terminal:

```
claude plugin marketplace add fibtecltd/fibtec-marketplace
claude plugin install etlgen@fibtec-marketplace
```

## What is in it

| Plugin | Product | What it does | Needs |
| --- | --- | --- | --- |
| `pyvar-mcp` | pyvar | All 385 pyvar functions as Claude Code tools, through the live API | A free pyvar API key ([pyvar.com](https://www.pyvar.com)); Claude Code only (it starts a local `uvx` server) |
| `pyvar-market-risk`, `pyvar-credit-risk`, `pyvar-liquidity-risk`, `pyvar-operational-risk`, `pyvar-portfolio-analytics`, `pyvar-regulatory`, `pyvar-derivatives`, `pyvar-alm` | pyvar | Skills that show Claude how to use each risk domain's functions | `pyvar-mcp` for the calls |
| `pyvar-arch-api-gateway`, `pyvar-arch-data-ingestion`, `pyvar-arch-compute`, `pyvar-arch-storage`, `pyvar-arch-observability` | pyvar | Architecture notes for people working on the pyvar codebase | Nothing |
| `etlgen` | ETL Integrator | Generate ETL scripts, REST and GraphQL connectors and webhook handlers | An ETL Integrator account |
| `tengrade` | TenGrade | Build, publish and manage exams and candidate instances; publishing and inviting candidates spend organisation credit | A TenGrade organisation account |

## Good to know

- **Use one marketplace per plugin.** pyvar's own marketplace (`pyvar-marketplace`) lists the same pyvar plugins and stays
  available. If you installed `pyvar-mcp@pyvar-marketplace`, keep it; adding the same plugin from here gives you a second
  copy under a different id. Plugin ids are `plugin@marketplace` and Claude Code has no migration for renaming a marketplace, which is why
  the old ones are not retired.
- **Updates are manual by default.** Third-party marketplaces do not update themselves: run
  `/plugin marketplace update fibtec-marketplace`, or turn on auto-update for it in `/plugin`.
- **What "installed from here" means.** Entries point at the default branch of each plugin's repository
  (`pyvar`: `master`, `fibtec-etlgen-plugin` and `fibtec-tengrade-plugin`: `main`), so you get the plugin as released
  there. An entry can be pinned to a commit with `sha` if a stricter policy is wanted.
- **Trust.** Anthropic does not review third-party marketplaces, and plugins can run code on your machine (MCP servers,
  hooks). Read what you install; every plugin's source is in the public repository named in its entry.

## For organisations

Register the marketplace and pre-install plugins for everyone through managed settings:

```json
{
  "extraKnownMarketplaces": {
    "fibtec-marketplace": { "source": { "source": "github", "repo": "fibtecltd/fibtec-marketplace" } }
  },
  "enabledPlugins": { "pyvar-mcp@fibtec-marketplace": true }
}
```

To allow only this marketplace (and your own), list its source in `strictKnownMarketplaces`. The allow-list matches the
marketplace's source, not each plugin's.

## Changing the catalogue

Changes go through pull requests. CI (`.github/workflows/validate.yml`) runs `claude plugin validate . --strict` and
`scripts/check_sources.py`, which asks each plugin's repository whether the Git ref the entry names still exists.

Report a problem with an issue in this repository. For a security matter write to the address in
[security.txt](https://fibtec.co.uk/.well-known/security.txt).

## Licence

Apache-2.0 (see `LICENSE`). Each plugin carries its own licence in its own repository.
