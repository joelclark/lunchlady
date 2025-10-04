#!/usr/bin/env python3
"""Lunch Lady - Meal Planning CLI App."""

import argparse
import sys
from pathlib import Path

from config import Config, ConfigError
from sheets_client import SheetsClient, SheetsClientError
from sheet_loader import load_sheet_data
from prompt_builder import PromptBuilder, load_prompt_files
from gemini_client import GeminiClient, GeminiClientError


# Get script directory
SCRIPT_DIR = Path(__file__).parent

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;205m'
    PURPLE = '\033[38;5;129m'
    LIME = '\033[38;5;118m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BG_BLACK = '\033[40m'

def print_banner():
    """Print the colorful Lunchlady banner"""
    
    banner = f"""
{Colors.BOLD}{Colors.BG_BLACK}
{Colors.RED}██╗     {Colors.ORANGE}██╗   ██╗{Colors.YELLOW}███╗   ██╗{Colors.GREEN} ██████╗{Colors.CYAN}██╗  ██╗{Colors.BLUE}██╗     {Colors.PURPLE} █████╗ {Colors.PINK}██████╗ {Colors.MAGENTA}██╗   ██╗
{Colors.RED}██║     {Colors.ORANGE}██║   ██║{Colors.YELLOW}████╗  ██║{Colors.GREEN}██╔════╝{Colors.CYAN}██║  ██║{Colors.BLUE}██║     {Colors.PURPLE}██╔══██╗{Colors.PINK}██╔══██╗{Colors.MAGENTA}╚██╗ ██╔╝
{Colors.RED}██║     {Colors.ORANGE}██║   ██║{Colors.YELLOW}██╔██╗ ██║{Colors.GREEN}██║     {Colors.CYAN}███████║{Colors.BLUE}██║     {Colors.PURPLE}███████║{Colors.PINK}██║  ██║{Colors.MAGENTA} ╚████╔╝ 
{Colors.RED}██║     {Colors.ORANGE}██║   ██║{Colors.YELLOW}██║╚██╗██║{Colors.GREEN}██║     {Colors.CYAN}██╔══██║{Colors.BLUE}██║     {Colors.PURPLE}██╔══██║{Colors.PINK}██║  ██║{Colors.MAGENTA}  ╚██╔╝  
{Colors.RED}███████╗{Colors.ORANGE}╚██████╔╝{Colors.YELLOW}██║ ╚████║{Colors.GREEN}╚██████╗{Colors.CYAN}██║  ██║{Colors.BLUE}███████╗{Colors.PURPLE}██║  ██║{Colors.PINK}██████╔╝{Colors.MAGENTA}   ██║   
{Colors.RED}╚══════╝{Colors.ORANGE} ╚═════╝ {Colors.YELLOW}╚═╝  ╚═══╝{Colors.GREEN} ╚═════╝{Colors.CYAN}╚═╝  ╚═╝{Colors.BLUE}╚══════╝{Colors.PURPLE}╚═╝  ╚═╝{Colors.PINK}╚═════╝ {Colors.MAGENTA}   ╚═╝   
{Colors.RESET}
{Colors.LIME}                   ╔════════════════════════════════════╗
{Colors.LIME}                   ║ {Colors.WHITE}🍔 Let's serve up a meal plan!! 🍕{Colors.LIME} ║
{Colors.LIME}                   ╚════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def log(msg):
    """Print to stderr."""
    print(msg, file=sys.stderr)


def main():
    """Main entry point for the CLI."""

    print_banner()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Generate meal plans using Google Sheets and Gemini'
    )
    parser.add_argument(
        '--env-file',
        default='.env',
        help='Path to .env file (default: .env)'
    )
    parser.add_argument(
        '--output',
        default='md',
        help='Output format (default: md). Maps to prompt-output-{format}.md'
    )
    args = parser.parse_args()

    try:
        # Load configuration
        log("📋 Loading configuration...")
        config = Config(env_file=args.env_file)
        log(f"✓ Using model: {config.gemini_model}\n")

        # Initialize Google Sheets client
        log("📊 Connecting to Google Sheets...")
        sheets_client = SheetsClient(
            api_key=config.google_api_key,
            spreadsheet_id=config.spreadsheet_id
        )

        # Load all sheet data
        log("📖 Reading 'config' sheet...")
        sheet_data = load_sheet_data(sheets_client)

        if sheet_data.config:
            log(f"✓ Found {len(sheet_data.config)} config value(s)")
        else:
            log("✓ No config sheet found (optional)")

        log("📖 Reading 'sheet-context' sheet...")
        if sheet_data.sheet_context:
            log(f"✓ Found context for {len(sheet_data.sheet_context)} sheet(s)")
        else:
            log("✓ No sheet-context found (optional)")

        log("\n🍽️  Reading food sheets...")
        for sheet_name, sheet_rows in sheet_data.food_sheets:
            row_count = len(sheet_rows) - 1 if sheet_rows else 0  # Subtract header row
            log(f"  • {sheet_name}: {row_count} items")

        log("\n🔨 Building prompt...")

        # Load optional prompt files
        prompt_top, prompt_output = load_prompt_files(SCRIPT_DIR, args.output)
        if prompt_top:
            log("  ✓ Found prompt-top.md")
        if not prompt_output:
            log(f"❌ Required output prompt file not found: prompt-output-{args.output}.md")
            sys.exit(1)
        log(f"  ✓ Found prompt-output-{args.output}.md")

        # Build prompt
        prompt_builder = PromptBuilder(
            config=sheet_data.config,
            sheet_context=sheet_data.sheet_context,
            food_sheets=sheet_data.food_sheets,
            prompt_top=prompt_top,
            prompt_output=prompt_output
        )
        prompt = prompt_builder.build_prompt()
        log(f"✓ Prompt assembled ({len(prompt)} characters)")

        # Save prompt to file
        prompt_file = SCRIPT_DIR / 'last-prompt.md'
        prompt_file.write_text(prompt)
        log("✓ Saved to last-prompt.md")

        # Initialize Gemini client and generate meal plan
        log(f"\n🤖 Calling Gemini ({config.gemini_model})...")
        gemini_client = GeminiClient(
            model=config.gemini_model,
            temperature=config.gemini_temperature,
            max_tokens=config.gemini_max_tokens
        )

        response = gemini_client.generate_meal_plan(prompt)

        log("✓ Response received")

        # Save response to file
        response_file = SCRIPT_DIR / f'last-response.{args.output}'
        response_file.write_text(response)
        log(f"✓ Saved to last-response.{args.output}\n")

        log("=" * 60 + "\n")

        # Print response to stdout
        print(response)

    except ConfigError as e:
        log(f"❌ Configuration error: {e}")
        sys.exit(1)
    except SheetsClientError as e:
        log(f"❌ Google Sheets error: {e}")
        sys.exit(1)
    except GeminiClientError as e:
        log(f"❌ Gemini error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        log("\n🛑 Cancelled by user")
        sys.exit(130)
    except Exception as e:
        log(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()