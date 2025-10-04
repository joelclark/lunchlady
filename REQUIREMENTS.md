# Lunch Lady - Meal Planning CLI App

## Overview
A Python CLI tool that generates meal plans by reading meal component data from Google Sheets, assembling a prompt with that data, and sending it to Google Gemini for meal planning suggestions.

## Technical Requirements
- Python 3.12+
- Modular architecture for future integration into larger app
- No UI - command line only
- Google Sheets as datastore
- Google Gemini API for meal plan generation
- Output uses informal language

## Google Sheets Structure

### Special Sheets (not rendered as data):

**1. "config" sheet**
- Two columns: key | value
- Recognized keys (all optional):
  - `prompt_header` - Static text at the start of the prompt (after prompt-top.md)
  - `prompt_footer` - Static text at the end of the prompt (after food sheets, before user_input)


**2. "sheet-context" sheet**
- Two columns: sheet_name | context
- Provides introductory context for each food sheet
- Optional - if a sheet isn't listed here, it just won't have context text

### Food Sheets:
- Any sheet that isn't "config" or "sheet-context"
- Simple tabular data with header row in first row
- Will be rendered as markdown tables in the prompt
- Rendered in the order they appear in the workbook

## Configuration (.env file)

Required environment variables:
- `GOOGLE_API_KEY` - Google API key (used for both Sheets and Gemini)
- `SPREADSHEET_ID` - Google Sheets workbook ID
- `GEMINI_MODEL` - Which Gemini model to use (e.g., "gemini-2.0-flash-exp", "gemini-1.5-pro")

Optional:
- `GEMINI_TEMPERATURE` - Sampling temperature (0.0-2.0)
- `GEMINI_MAX_TOKENS` - Maximum tokens in response

## CLI Interface

**Usage:**
```bash
python main.py [--env-file PATH]
```

**Arguments:**
- `--env-file` - Optional path to .env file (defaults to `.env` in current directory)

**Output:**
- Prints Gemini response to stdout
- Saves assembled prompt to `last-prompt.md`
- Saves Gemini response to `last-response.md`

## Optional Prompt Files

Two optional markdown files can be placed in the project root:
- `prompt-top.md` - Content injected at the very beginning of the prompt
- `prompt-output-markdown.md` - Content injected at the very end of the prompt

These wrap around the config sheet's prompt_header and prompt_footer.

## Prompt Structure

The assembled prompt will follow this format:

```
{prompt-top.md if exists}

{config["prompt_header"] if exists}

## [Sheet Name 1]
{sheet-context for Sheet Name 1, if exists}

[markdown table of Sheet 1 data including headers]

## [Sheet Name 2]
{sheet-context for Sheet Name 2, if exists}

[markdown table of Sheet 2 data including headers]

...

{config["prompt_footer"] if exists}

**Final thoughts from the user:** {config["user_input"] if exists}

{prompt-output-markdown.md if exists}
```

## Module Structure

### 1. `config.py`
- Load and parse .env file
- Validate required environment variables
- Provide access to configuration values
- Handle --env-file command line argument

### 2. `sheets_client.py`
- Authenticate with Google Sheets API using API key
- Connect to specified spreadsheet
- Get ordered list of all sheet names
- Read "config" sheet into dict (key -> value)
- Read "sheet-context" sheet into dict (sheet_name -> context)
- Read any sheet's data as tabular format (list of lists)
- Preserve sheet order from workbook

### 3. `sheet_loader.py`
- Orchestrate data loading from Google Sheets
- Return SheetData dataclass containing config, sheet_context, and food_sheets
- Acts as facade over sheets_client.py

### 4. `prompt_builder.py`
- Accept config dict, sheet-context dict, and ordered list of sheet data
- Accept optional prompt-top.md and prompt-output-markdown.md content
- Format each food sheet as markdown table (with headers)
- Add sheet context before each table if available
- Assemble full prompt: prompt-top + header + all sheets + footer + user_input + prompt-output
- Return complete prompt string

### 5. `gemini_client.py`
- Initialize with model name
- Accept prompt text
- Call Gemini API with configured parameters
- Return response text
- Handle API errors gracefully

### 6. `main.py`
- CLI entry point
- Parse command line arguments
- Load configuration
- Initialize sheets client and get data from all sheets
- Read optional prompt-top.md and prompt-output-markdown.md files
- Build prompt using prompt builder
- Save assembled prompt to last-prompt.md
- Call Gemini client
- Save response to last-response.md
- Print response to stdout
- Handle errors and provide helpful messages

## Setup Instructions (to be provided to user)

Documentation needed for:
1. How to create a Google Sheets API key
2. How to get the Spreadsheet ID from a Google Sheets URL
3. How to structure the .env file
4. Example config and sheet-context sheet structures
5. Installation (pip install requirements)

