#!/usr/bin/env python3
"""Lunch Lady - Meal Planning CLI App."""

import argparse
import sys
from pathlib import Path

from config import Config, ConfigError
from sheets_client import SheetsClientError
from gemini_client import GeminiClientError
from meal_plan_generator import MealPlanGenerator


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

        log("🔨 Generating meal plan...")

        # Generate meal plan using shared generator
        generator = MealPlanGenerator(config, SCRIPT_DIR)
        result = generator.generate(output_format=args.output)

        log(f"✓ Prompt assembled ({len(result.prompt)} characters)")

        # Save prompt to file
        prompt_file = SCRIPT_DIR / 'last-prompt.md'
        prompt_file.write_text(result.prompt)
        log("✓ Saved to last-prompt.md")

        log(f"\n🤖 Response received")

        # Save response to file
        response_file = SCRIPT_DIR / f'last-response.{result.output_format}'
        response_file.write_text(result.response)
        log(f"✓ Saved to last-response.{result.output_format}\n")

        log("=" * 60 + "\n")

        # Print response to stdout
        print(result.response)

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