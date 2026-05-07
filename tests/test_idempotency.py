from sheets_airtable_sync.idempotency import make_idempotency_key, make_merge_key, stable_hash


def test_stable_keys_are_deterministic() -> None:
    assert stable_hash({"b": 2, "a": 1}) == stable_hash({"a": 1, "b": 2})
    assert make_merge_key({"Email": "A@EXAMPLE.COM"}, ["Email"]) == "a@example.com"
    assert make_idempotency_key("crm", "a", {"x": 1}).startswith("crm:a:")
