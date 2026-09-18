# ROH-Bench v0.1

Residual Obstruction Hypothesis Benchmark — 100 synthetic worlds

This repository implements the first synthetic experiment for the Residual Obstruction Hypothesis (ROH).

> **Research question:** When an agent encounters persistent, structured prediction residuals caused by a hidden change in the world's rule, does explicitly preserving the unresolved residuals and revising the working model without erasing local evidence improve adaptation and transfer relative to an otherwise matched collapse/update architecture?

## Experimental design

- 100 deterministic synthetic worlds
- 20 worlds each from five hidden-rule families: threshold, parity, conjunction, relational, piecewise
- 300 episodes per world
- Phase A (1–80): learn original rule
- Phase B (81–120): hidden rule change + obstruction events + isolated noise residuals
- Phase C (121–180): adaptation
- Phase D (181–240): stability / backward retention
- Phase E (241–300): structural transfer
- Matched Collapse and ROH agents
- Primary metric: **Post-Obstruction Cumulative Error (POCE)**

## Primary hypothesis

**H0:** ROH does not reduce POCE relative to Collapse.

**H1:** ROH reduces POCE relative to Collapse.

The benchmark is deliberately falsifiable. No composite “ROH score” is used.

## Run

```bash
python -m roh.runner --condition both --worlds 100 --episodes 300 --seed 10000 --output results
python -m roh.metrics --collapse results/collapse.json --roh results/roh.json
```

Smoke test:

```bash
python -m roh.runner --condition both --worlds 2 --episodes 300 --seed 10000 --output results/smoke
```

## Metrics

1. POCE — primary adaptation endpoint
2. T90 — episodes to 90% rolling accuracy
3. OR — obstruction retention
4. FOR — false obstruction rate
5. RR — residual recurrence
6. TA — transfer accuracy
7. BR — backward retention
8. CM — model-revision efficiency
9. ORT — obstruction resolution time

The analysis is paired by world because both conditions receive identical generated worlds and episode streams.

## Scientific status

This repository does **not** claim that ROH is sufficient for AGI, or that a positive synthetic result establishes general intelligence. It tests a narrower architectural hypothesis under controlled distribution shifts.

## Project

**time8machine / Undergraduate Intelligence Initiative**

Date: 18 September 2026

License: MIT
