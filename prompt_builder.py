"""Prompt builder for Lunch Lady."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_prompt_files(script_dir: Path, output_format: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Load optional prompt-top.md and prompt-output-{format}.md files.

    Args:
        script_dir: Directory to search for prompt files
        output_format: Output format name (e.g., 'markdown', 'json')

    Returns:
        Tuple of (prompt_top, prompt_output), each may be None if file doesn't exist
    """
    prompt_top = None
    prompt_top_file = script_dir / 'prompt-top.md'
    if prompt_top_file.exists():
        prompt_top = prompt_top_file.read_text()

    prompt_output = None
    prompt_output_file = script_dir / f'prompt-output-{output_format}.md'
    if prompt_output_file.exists():
        prompt_output = prompt_output_file.read_text()

    return prompt_top, prompt_output


class PromptBuilder:
    """Builds prompts from Google Sheets data."""

    def __init__(
        self,
        config: Dict[str, str],
        sheet_context: Dict[str, str],
        food_sheets: List[Tuple[str, List[List[str]]]],
        prompt_top: Optional[str] = None,
        prompt_output: Optional[str] = None
    ):
        """
        Initialize the prompt builder.

        Args:
            config: Configuration dictionary from config sheet
            sheet_context: Sheet context dictionary
            food_sheets: List of (sheet_name, sheet_data) tuples
            prompt_top: Optional content to inject at the very top
            prompt_output: Optional content to inject at the very bottom
        """
        self.config = config
        self.sheet_context = sheet_context
        self.food_sheets = food_sheets
        self.prompt_top = prompt_top
        self.prompt_output = prompt_output

    def build_prompt(self) -> str:
        """
        Build the complete prompt.

        Returns:
            The assembled prompt string.
        """
        parts = []

        # Add top file content
        if self.prompt_top:
            parts.append(self.prompt_top)
            parts.append('')  # Empty line

        # Add header from config
        if 'prompt_header' in self.config:
            parts.append(self.config['prompt_header'])
            parts.append('')  # Empty line

        # Add each food sheet
        for sheet_name, sheet_data in self.food_sheets:
            parts.append(f"## {sheet_name}")

            # Add context if available
            if sheet_name in self.sheet_context:
                parts.append(self.sheet_context[sheet_name])
                parts.append('')  # Empty line

            # Add markdown table
            if sheet_data:
                table = self._format_as_markdown_table(sheet_data)
                parts.append(table)
            else:
                parts.append('(No data)')

            parts.append('')  # Empty line between sheets

        # Add footer from config
        if 'prompt_footer' in self.config:
            parts.append(self.config['prompt_footer'])
            parts.append('')  # Empty line

        # Add user input from config
        if 'user_input' in self.config:
            parts.append('**Final thoughts from the user:** ' + self.config['user_input'])
            parts.append('')  # Empty line

        # Add output file content
        if self.prompt_output:
            parts.append(self.prompt_output)
            parts.append('')  # Empty line

        return '\n'.join(parts)

    def _format_as_markdown_table(self, data: List[List[str]]) -> str:
        """
        Format sheet data as a markdown table.

        Args:
            data: Sheet data with header row first

        Returns:
            Markdown formatted table string.
        """
        if not data:
            return ''

        # Get column count from first row
        num_cols = len(data[0])

        # Pad rows to ensure they all have the same number of columns
        normalized_data = []
        for row in data:
            padded_row = row + [''] * (num_cols - len(row))
            normalized_data.append(padded_row[:num_cols])

        lines = []

        # Header row
        header = normalized_data[0]
        lines.append('| ' + ' | '.join(header) + ' |')

        # Separator row
        lines.append('| ' + ' | '.join(['---'] * num_cols) + ' |')

        # Data rows
        for row in normalized_data[1:]:
            lines.append('| ' + ' | '.join(row) + ' |')

        return '\n'.join(lines)