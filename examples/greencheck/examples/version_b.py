"""Candidate: use the closed-form sum-of-squares formula."""

N = 1_000_000


def run() -> int:
    n = N
    return (n - 1) * n * (2 * n - 1) // 6
