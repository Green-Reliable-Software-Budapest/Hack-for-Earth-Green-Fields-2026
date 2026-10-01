"""Baseline: materialise every square before summing it."""

N = 1_000_000


def run() -> int:
    squares = [number * number for number in range(N)]
    return sum(squares)
