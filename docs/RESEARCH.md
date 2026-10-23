# Engineering research

Reviewed 2026-10-23. These references inform design decisions; the project implementation is original, not copied source code.

## Primary references

- https://docs.python.org/3/library/graphlib.html

## Application to this project

Kahn-style traversal tracks predecessor counts and processes a min-heap of ready IDs. Earliest finish propagates forward. A reverse pass calculates latest starts from successors, then subtracts earliest starts to find slack. Impact analysis computes the transitive descendants of a changed task. Randomized tests compare valid node coverage and dependency order with Python graphlib.TopologicalSorter.

## What this does not establish

Using an established pattern does not establish novelty, production readiness, or measured business impact. Tests validate bounded scenarios, not every operating condition. All examples are synthetic. The browser implementation and Python implementation run in different environments and are documented separately.
