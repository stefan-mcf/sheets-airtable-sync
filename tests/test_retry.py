from sheets_airtable_sync.clients.retry import retry_decision


def test_retry_after_and_non_retryable() -> None:
    assert retry_decision(429, 1, retry_after="5").delay_seconds == 5
    assert retry_decision(400, 1).should_retry is False
    assert retry_decision(503, 2).should_retry is True
