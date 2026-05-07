from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryDecision:
    should_retry: bool
    delay_seconds: float
    reason: str


RETRYABLE_STATUSES = {408, 409, 425, 429, 500, 502, 503, 504}


def retry_decision(status_code: int, attempt: int, retry_after: str | None = None, base_delay: float = 1.0, max_delay: float = 60.0) -> RetryDecision:
    if status_code not in RETRYABLE_STATUSES:
        return RetryDecision(False, 0.0, "not_retryable")
    if retry_after:
        try:
            return RetryDecision(True, min(float(retry_after), max_delay), "retry_after")
        except ValueError:
            pass
    delay = min(base_delay * (2 ** max(attempt - 1, 0)), max_delay)
    jitter = min(0.25 * attempt, 2.0)
    return RetryDecision(True, delay + jitter, "exponential_backoff")
