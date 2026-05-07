from sheets_airtable_sync.config import load_mapping, load_rows


def test_load_mapping_and_rows() -> None:
    mapping = load_mapping("configs/mappings/leads-to-airtable.json")
    rows = load_rows("examples/input/crm-leads.json")
    assert mapping.scenario == "crm-leads"
    assert rows
