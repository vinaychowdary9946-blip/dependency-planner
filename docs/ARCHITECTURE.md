# Architecture and decisions

## Use case

A release checklist can hide cycles, missing dependencies, and work that has no scheduling slack. This tool validates a dependency graph and calculates the earliest feasible schedule.

## Core design

Kahn-style traversal tracks predecessor counts and processes a min-heap of ready IDs. Earliest finish propagates forward. A reverse pass calculates latest starts from successors, then subtracts earliest starts to find slack. Impact analysis computes the transitive descendants of a changed task. Randomized tests compare valid node coverage and dependency order with Python graphlib.TopologicalSorter.

## Tradeoffs

Durations are supplied estimates in consistent units, not predictions. The plan assumes unlimited parallel resources, no holidays, no resource contention, and no uncertainty. Zero-slack tasks may form multiple critical paths. Cycle errors identify blocked tasks, including descendants, rather than a minimal cycle witness. Up to 1,000 tasks are accepted. The Python planner uses a heap to choose ready tasks deterministically.

## Runtime boundaries

The Python engine is the durable implementation. The browser simulation demonstrates the same domain concepts with synthetic data and an in-memory clock or event list; it is not a hosted distributed service. POST /api exposes Python behavior locally. The development server binds to loopback only and rejects foreign browser origins. It has no authentication, rate limiting, TLS, or service manager: do not expose it directly to the internet.

## Operational considerations

Keep databases on local disks and back up with SQLite's backup API or a controlled shutdown; do not copy an active database without its WAL state. Test restoration before relying on backups. Do not write credentials or personal data into example payloads. For a public deployment, place an authenticated application server behind TLS, implement request quotas, structured logs, monitoring and access controls, and exercise recovery under load. No production throughput or SLA is claimed.
