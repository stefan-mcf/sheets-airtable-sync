from sheets_airtable_sync.models import FieldMapping, MappingConfig, ReasonCode


def test_mapping_config_model() -> None:
    cfg = MappingConfig(scenario="x", merge_key_fields=["Email"], fields=[FieldMapping(source_field="email", target_field="Email", transform="email", required=True, merge_key=True)])
    assert cfg.fields[0].merge_key is True
    assert ReasonCode.MISSING_REQUIRED_FIELD.value == "missing_required_field"
