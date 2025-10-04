# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lunch Lady is a Python CLI tool that generates meal plans by:
1. Reading meal component data from Google Sheets
2. Assembling a structured prompt from sheet data and optional template files
3. Sending the prompt to Google Gemini API for meal planning suggestions
4. Outputting the meal plan to stdout and saving it to `last-response.md`

## Commands

**Setup:**
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# .venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with actual GOOGLE_API_KEY, SPREADSHEET_ID, GEMINI_MODEL
```

**Run:**
```bash
python main.py                        # Use default .env file
python main.py --env-file /path/.env  # Use custom .env file
```

## Architecture

### Data Flow Pipeline
1. **Config Loading** (`config.py`) - Parses `.env` file, validates required vars
2. **Sheets Client** (`sheets_client.py`) - Authenticates with Google Sheets API using API key
3. **Sheet Loader** (`sheet_loader.py`) - Orchestrates loading, returns `SheetData` dataclass
4. **Prompt Builder** (`prompt_builder.py`) - Assembles final prompt from multiple sources
5. **Gemini Client** (`gemini_client.py`) - Calls Google Gemini API with assembled prompt
6. **Main** (`main.py`) - CLI entry point that coordinates the pipeline

### Key Design Patterns

**Special Sheets**: The sheets client treats two sheet names specially:
- `config` - Two-column key-value pairs (e.g., `prompt_header`, `prompt_footer`, `user_input`)
- `sheet-context` - Maps sheet names to introductory context text
- All other sheets are "food sheets" and rendered as markdown tables

**Prompt Assembly Order**:
```
1. prompt-top.md (optional file)
2. config["prompt_header"] (optional sheet value)
3. For each food sheet:
   - ## Sheet Name
   - sheet-context[sheet_name] (optional)
   - Markdown table of sheet data
4. config["prompt_footer"] (optional sheet value)
5. **Final thoughts from the user:** config["user_input"] (optional)
6. prompt-output-{format}.md (optional file - format is configurable, CLI uses "markdown")
```

**Output Files**:
- `last-prompt.md` - The full assembled prompt sent to Gemini
- `last-response.md` - The response from Gemini API

### Module Responsibilities

- `config.py`: Environment variable management, validates `GOOGLE_API_KEY`, `SPREADSHEET_ID`, `GEMINI_MODEL`
- `sheets_client.py`: Low-level Google Sheets API operations, preserves sheet order from workbook
- `sheet_loader.py`: Facade over sheets_client, returns `SheetData` dataclass containing all loaded data
- `prompt_builder.py`: Markdown table formatting, prompt assembly from multiple sources; `load_prompt_files()` accepts an output format parameter to load `prompt-output-{format}.md`
- `gemini_client.py`: Google Gemini API client with configurable temperature and max_tokens
- `main.py`: CLI orchestration, error handling, progress logging to stderr; currently uses "markdown" as the output format

### Configuration

Required `.env` variables:
- `GOOGLE_API_KEY` - Used for both Sheets API and Gemini API
- `SPREADSHEET_ID` - The ID from the Google Sheets URL
- `GEMINI_MODEL` - Model name (e.g., `gemini-2.0-flash-exp`, `gemini-1.5-pro`)

Optional `.env` variables:
- `GEMINI_TEMPERATURE` - Sampling temperature (0.0-2.0)
- `GEMINI_MAX_TOKENS` - Maximum tokens in response

### Error Handling

Custom exceptions for each module:
- `ConfigError` - Missing/invalid environment variables
- `SheetsClientError` - Google Sheets API failures
- `GeminiClientError` - Gemini API failures

All errors are caught in `main.py` and result in user-friendly messages logged to stderr before exiting.

## Important Notes

- The Google API key must have access to both Google Sheets API and Generative Language API
- The spreadsheet must be set to "Anyone with the link can view" for API key access to work
- Progress messages are logged to stderr (via `log()` function), final response goes to stdout
- The `openai_client.py` file exists in the repo but is not currently used
