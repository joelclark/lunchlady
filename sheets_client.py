"""Google Sheets client for Lunch Lady."""

from typing import Dict, List, Optional, Tuple
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SheetsClientError(Exception):
    """Raised when there's an error accessing Google Sheets."""
    pass


class SheetsClient:
    """Client for reading data from Google Sheets."""

    SPECIAL_SHEETS = {'config', 'sheet-context'}

    def __init__(self, api_key: str, spreadsheet_id: str):
        """
        Initialize the Sheets client.

        Args:
            api_key: Google API key
            spreadsheet_id: ID of the spreadsheet to read from
        """
        self.api_key = api_key
        self.spreadsheet_id = spreadsheet_id
        self.service = build('sheets', 'v4', developerKey=api_key)

    def get_all_sheet_names(self) -> List[str]:
        """
        Get ordered list of all sheet names in the spreadsheet.

        Returns:
            List of sheet names in the order they appear in the workbook.
        """
        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()

            return [sheet['properties']['title'] for sheet in spreadsheet['sheets']]
        except HttpError as e:
            raise SheetsClientError(f"Failed to get sheet names: {e}")

    def read_sheet(self, sheet_name: str) -> List[List[str]]:
        """
        Read all data from a sheet.

        Args:
            sheet_name: Name of the sheet to read

        Returns:
            List of rows, where each row is a list of cell values.
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=sheet_name
            ).execute()

            return result.get('values', [])
        except HttpError as e:
            raise SheetsClientError(f"Failed to read sheet '{sheet_name}': {e}")

    def read_config_sheet(self) -> Dict[str, str]:
        """
        Read the 'config' sheet and return as a dictionary.

        Returns:
            Dictionary mapping config keys to values.
            Returns empty dict if sheet doesn't exist.
        """
        try:
            data = self.read_sheet('config')
        except SheetsClientError:
            # config sheet is optional
            return {}

        if not data:
            return {}

        config = {}
        for row in data:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                config[key] = value

        return config

    def read_sheet_context(self) -> Dict[str, str]:
        """
        Read the 'sheet-context' sheet and return as a dictionary.

        Returns:
            Dictionary mapping sheet names to their context text.
            Returns empty dict if sheet doesn't exist.
        """
        try:
            data = self.read_sheet('sheet-context')
        except SheetsClientError:
            # sheet-context is optional
            return {}

        if not data:
            return {}

        context = {}
        for row in data:
            if len(row) >= 2:
                sheet_name = row[0].strip()
                context_text = row[1].strip()
                context[sheet_name] = context_text

        return context

    def get_food_sheets_data(self) -> List[Tuple[str, List[List[str]]]]:
        """
        Get all food sheets (non-special sheets) with their data.

        Returns:
            List of tuples (sheet_name, sheet_data) in workbook order.
        """
        all_sheets = self.get_all_sheet_names()
        food_sheets = []

        for sheet_name in all_sheets:
            if sheet_name not in self.SPECIAL_SHEETS:
                data = self.read_sheet(sheet_name)
                food_sheets.append((sheet_name, data))

        return food_sheets