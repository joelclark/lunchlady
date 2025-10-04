"""Sheet data loader module."""

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
from sheets_client import SheetsClient


@dataclass
class SheetData:
    """Container for all loaded sheet data."""
    config: Optional[Dict[str, str]]
    sheet_context: Optional[Dict[str, str]]
    food_sheets: List[Tuple[str, List[List[str]]]]


def load_sheet_data(sheets_client: SheetsClient) -> SheetData:
    """Load all data from Google Sheets.

    Args:
        sheets_client: Initialized SheetsClient instance

    Returns:
        SheetData containing config, sheet_context, and food_sheets
    """
    # Read config sheet
    config = sheets_client.read_config_sheet()

    # Read sheet context
    sheet_context = sheets_client.read_sheet_context()

    # Read all food sheets
    food_sheets = sheets_client.get_food_sheets_data()

    return SheetData(
        config=config,
        sheet_context=sheet_context,
        food_sheets=food_sheets
    )
