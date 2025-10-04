"""Core meal plan generation logic for Lunch Lady."""

from pathlib import Path
from typing import Optional, Tuple
from dataclasses import dataclass

from config import Config
from sheets_client import SheetsClient
from sheet_loader import load_sheet_data
from prompt_builder import PromptBuilder, load_prompt_files
from gemini_client import GeminiClient


@dataclass
class GenerationResult:
    """Result of a meal plan generation."""
    response: str
    prompt: str
    output_format: str


class MealPlanGenerator:
    """Generates meal plans using the full pipeline."""

    def __init__(self, config: Config, script_dir: Path):
        """
        Initialize the generator.

        Args:
            config: Configuration object
            script_dir: Directory containing prompt files
        """
        self.config = config
        self.script_dir = script_dir

    def generate(self, output_format: str = 'md') -> GenerationResult:
        """
        Generate a meal plan.

        Args:
            output_format: Output format (e.g., 'md', 'html')

        Returns:
            GenerationResult containing the response, prompt, and format
        """
        # Initialize Google Sheets client
        sheets_client = SheetsClient(
            api_key=self.config.google_api_key,
            spreadsheet_id=self.config.spreadsheet_id
        )

        # Load all sheet data
        sheet_data = load_sheet_data(sheets_client)

        # Load prompt files
        prompt_top, prompt_output = load_prompt_files(self.script_dir, output_format)

        if not prompt_output:
            raise ValueError(f"Required output prompt file not found: prompt-output-{output_format}.md")

        # Build prompt
        prompt_builder = PromptBuilder(
            config=sheet_data.config,
            sheet_context=sheet_data.sheet_context,
            food_sheets=sheet_data.food_sheets,
            prompt_top=prompt_top,
            prompt_output=prompt_output
        )
        prompt = prompt_builder.build_prompt()

        # Initialize Gemini client and generate meal plan
        gemini_client = GeminiClient(
            model=self.config.gemini_model,
            temperature=self.config.gemini_temperature,
            max_tokens=self.config.gemini_max_tokens
        )

        response = gemini_client.generate_meal_plan(prompt)

        return GenerationResult(
            response=response,
            prompt=prompt,
            output_format=output_format
        )
