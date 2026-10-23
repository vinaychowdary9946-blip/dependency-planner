# Dependency Planner

A release checklist can hide cycles, missing dependencies, and work that has no scheduling slack. This tool validates a dependency graph and calculates the earliest feasible schedule.

Independent engineering project built around realistic failure scenarios. Examples use synthetic data; no customer deployment or commercial impact is claimed.

**[Live interactive demo](https://vinaychowdary9946-blip.github.io/demos/dependency-planner/)** · [Architecture](docs/ARCHITECTURE.md) · [API guide](docs/API.md) · [Verification](docs/VERIFICATION.md)

## What it does

Deterministic topological ordering; cycle and missing-node rejection; earliest starts; latest starts and total slack; critical tasks; downstream change-impact analysis.

## Run locally

Requires Python 3.10+; no pip installation, paid service, or API key is required. From this repository directory:

```sh
python planner.py examples/release.json
python planner.py examples/release.json --impact api
python -m unittest discover -s tests -v
python server.py
```

Open http://127.0.0.1:8000 for the browser simulation. The local server also exposes POST /api for the actual Python engine; see [API examples](docs/API.md). The visual simulation is deliberately separate from the backend and keeps its data in browser memory. Reloading clears it. SQLite files persist local API and CLI data across restarts.

## Repository map

- `planner.py` — domain implementation and CLI
- `server.py` — loopback development server and JSON API
- `web/` — interactive browser simulation, no dependencies
- `tests/` — domain, concurrency, and HTTP tests
- `examples/` — reproducible inputs
- `docs/` — architecture, API contracts, research, validation, and operations

## Engineering boundaries

Durations are supplied estimates in consistent units, not predictions. The plan assumes unlimited parallel resources, no holidays, no resource contention, and no uncertainty. Zero-slack tasks may form multiple critical paths. Cycle errors identify blocked tasks, including descendants, rather than a minimal cycle witness. Up to 1,000 tasks are accepted. The Python planner uses a heap to choose ready tasks deterministically.

## Development

Run tests from the repository root. GitHub Actions is configured for Python 3.10, 3.12, and 3.13 on Linux and Windows. Local validation and hosted CI results are reported separately in the verification guide.

MIT license. Contributions should include a reproducible failing scenario and a regression test.
