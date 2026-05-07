"""Fixture-safe Sheets/Airtable sync proof package."""

from sheets_airtable_sync.sync import (
    list_scenarios,
    run_scenario,
    sync_rows,
    sync_rows_with_mapping,
)

__all__ = ["list_scenarios", "run_scenario", "sync_rows", "sync_rows_with_mapping"]
__version__ = "0.2.0"
