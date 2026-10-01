# GreenCheck

> **Organizer example — not an eligible competition entry.**

GreenCheck is a deliberately small reference project for **HACK4EARTH 2.0 — Greener Fields**.

It demonstrates one principle:

> Make the claim no larger than the evidence.

GreenCheck compares two Python implementations of the same task and reports:

- median wall-clock execution time
- median traced Python memory peak
- relative change between a baseline and candidate

It does **not** measure energy consumption or carbon emissions directly.

## Why this example exists

Hack for Earth accepts many kinds of technical projects. They do not all need sophisticated measurement systems.

The purpose of GreenCheck is to show how a team can:

1. define a narrow technical claim
2. run a repeatable comparison
3. document the test conditions
4. state limitations clearly
5. avoid turning a small benchmark into a larger sustainability claim

## Try it

Requires Python 3.10+ and no third-party packages.

From the repository root:

```bash
python examples/greencheck/greencheck.py   examples/greencheck/examples/version_a.py   examples/greencheck/examples/version_b.py   --runs 5
```

You should see output similar to:

```text
GreenCheck
==========================================================
Runs per implementation: 5
Metric                            Baseline     Candidate
----------------------------------------------------------
Median wall time (ms)              ...            ...
Median traced peak (KiB)           ...            ...
----------------------------------------------------------
Wall-time change: ...
Traced-memory change: ...

Scope: traced memory covers Python allocations observed by tracemalloc.
These measurements do not directly measure energy use or carbon emissions.
```

Exact values will vary by machine and operating conditions.

## The two implementations

The example compares two ways of calculating the sum of squares from `0` to `999,999`.

- `version_a.py` builds an in-memory list and sums it.
- `version_b.py` uses a closed-form mathematical expression.

Both return the same result.

The comparison is intentionally obvious so the measurement behaviour is easy to understand.

## What can we claim?

A reasonable claim is:

> Under the documented test conditions, the candidate completed the same task faster and with a lower traced Python allocation peak.

A claim GreenCheck does **not** establish is:

> The candidate is 80% greener.

Wall time and Python allocation measurements are not equivalent to energy consumption, lifecycle impact or carbon emissions.

## Limitations

- `tracemalloc` observes Python memory allocations, not total process or system memory.
- wall-clock timing is affected by hardware, operating system activity and other workloads
- this example does not isolate CPU frequency, thermal conditions or background processes
- it does not measure electricity consumption
- it does not convert results into carbon emissions

A stronger study would add appropriate energy instrumentation and document the test environment in more detail.

## Run the tests

```bash
python -m unittest discover -s examples/greencheck/tests -v
```

## Licence

GreenCheck is part of the Hack for Earth 2026 repository and is covered by the repository's Apache-2.0 licence.
