# Lunch Lady - Meal Planning CLI App

## Overview
A Python CLI tool that generates meal plans by reading meal component data from Google Sheets, assembling a prompt with that data, and sending it to OpenAI for meal planning suggestions.

## Technical Requirements
- Python 3.12+
- Modular architecture for future integration into larger app
- No UI - command line only
- Google Sheets as datastore
- OpenAI API for meal plan generation
- Output uses informal language

## Google Sheets Structure

### Special Sheets (not rendered as data):

**1. "config" sheet**
- Two columns: key | value
- Required keys:
  - `prompt_header` - Static text at the start of the prompt
  - `prompt_footer` - Static text at the end of the prompt
- Additional keys can be added as needed

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
- `GOOGLE_API_KEY` - Google Sheets API key
- `OPENAI_API_KEY` - OpenAI API key
- `SPREADSHEET_ID` - Google Sheets workbook ID
- `OPENAI_MODEL` - Which OpenAI model to use (e.g., "gpt-4", "gpt-3.5-turbo")

Optional:
- Additional OpenAI parameters as needed (temperature, max_tokens, etc.)

## CLI Interface

**Usage:**
```bash
python main.py [--env-file PATH]
```

**Arguments:**
- `--env-file` - Optional path to .env file (defaults to `.env` in current directory)

**Output:**
- Prints OpenAI response to stdout

## Prompt Structure

The assembled prompt will follow this format:

```
{config["prompt_header"]}

## [Sheet Name 1]
{sheet-context for Sheet Name 1, if exists}

[markdown table of Sheet 1 data including headers]

## [Sheet Name 2]
{sheet-context for Sheet Name 2, if exists}

[markdown table of Sheet 2 data including headers]

...

{config["prompt_footer"]}
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

### 3. `prompt_builder.py`
- Accept config dict, sheet-context dict, and ordered list of sheet data
- Format each food sheet as markdown table (with headers)
- Add sheet context before each table if available
- Assemble full prompt: header + all sheets + footer
- Return complete prompt string

### 4. `openai_client.py`
- Initialize with API key and model name
- Accept prompt text
- Call OpenAI API with configured parameters
- Return response text
- Handle API errors gracefully

### 5. `main.py`
- CLI entry point
- Parse command line arguments
- Load configuration
- Initialize sheets client and get data from all sheets
- Build prompt using prompt builder
- Call OpenAI client
- Print response to stdout
- Handle errors and provide helpful messages

## Setup Instructions (to be provided to user)

Documentation needed for:
1. How to create a Google Sheets API key
2. How to get the Spreadsheet ID from a Google Sheets URL
3. How to structure the .env file
4. Example config and sheet-context sheet structures
5. Installation (pip install requirements)

