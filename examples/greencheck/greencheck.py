#!/usr/bin/env python3
"""Compare two Python implementations using small, reproducible measurements."""

from __future__ import annotations

import argparse
import gc
import importlib.util
import statistics
import time
import tracemalloc
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class Measurement:
    elapsed_ms: float
    peak_kib: float
    result: Any


def load_run_function(path: Path, module_name: str) -> Callable[[], Any]:
    """Load a run() function from a Python file."""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValueError(f"Could not load {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    run = getattr(module, "run", None)
    if not callable(run):
        raise ValueError(f"{path} must define a callable run() function")
    return run


def measure(run: Callable[[], Any]) -> Measurement:
    """Measure one call using wall time and Python allocation tracing."""
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()

    try:
        result = run()
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

    return Measurement(
        elapsed_ms=elapsed_ms,
        peak_kib=peak_bytes / 1024,
        result=result,
    )


def benchmark(run: Callable[[], Any], runs: int) -> list[Measurement]:
    """Run a callable repeatedly."""
    return [measure(run) for _ in range(runs)]


def median(values: list[float]) -> float:
    return statistics.median(values)


def percent_change(baseline: float, candidate: float) -> float:
    if baseline == 0:
        return 0.0
    return ((candidate - baseline) / baseline) * 100


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare two Python implementations that each expose run()."
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be at least 1")

    baseline_run = load_run_function(args.baseline, "greencheck_baseline")
    candidate_run = load_run_function(args.candidate, "greencheck_candidate")

    baseline = benchmark(baseline_run, args.runs)
    candidate = benchmark(candidate_run, args.runs)

    if baseline[0].result != candidate[0].result:
        print("ERROR: implementations returned different results.")
        return 2

    baseline_time = median([m.elapsed_ms for m in baseline])
    candidate_time = median([m.elapsed_ms for m in candidate])
    baseline_memory = median([m.peak_kib for m in baseline])
    candidate_memory = median([m.peak_kib for m in candidate])

    print("GreenCheck")
    print("=" * 58)
    print(f"Runs per implementation: {args.runs}")
    print(f"{'Metric':<28}{'Baseline':>14}{'Candidate':>14}")
    print("-" * 58)
    print(f"{'Median wall time (ms)':<28}{baseline_time:>14.3f}{candidate_time:>14.3f}")
    print(f"{'Median traced peak (KiB)':<28}{baseline_memory:>14.1f}{candidate_memory:>14.1f}")
    print("-" * 58)
    print(f"Wall-time change: {percent_change(baseline_time, candidate_time):+.1f}%")
    print(f"Traced-memory change: {percent_change(baseline_memory, candidate_memory):+.1f}%")
    print()
    print("Scope: traced memory covers Python allocations observed by tracemalloc.")
    print("These measurements do not directly measure energy use or carbon emissions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
