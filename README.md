# Lunch Lady - Meal Planning CLI App

A Python CLI tool that generates meal plans by reading meal component data from Google Sheets and sending it to Google Gemini for intelligent meal planning suggestions.

## What It Does

Lunch Lady:
1. Connects to your Google Sheets spreadsheet containing meal components (proteins, vegetables, grains, etc.)
2. Reads configuration and food data from multiple sheets
3. Assembles a formatted prompt with all your meal options
4. Sends the prompt to Google Gemini to generate personalized meal plans
5. Outputs the meal plan suggestions to your terminal

## Setup Instructions

### 1. Set Up Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Your Google API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the required APIs:
   - Click "Enable APIs and Services"
   - Search for and enable "Google Sheets API"
   - Search for and enable "Generative Language API" (for Gemini)
4. Create an API Key:
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" → "API Key"
   - Copy the generated API key
   - (Optional but recommended) Click "Restrict Key" and limit it to Google Sheets API and Generative Language API

### 3. Get Your Spreadsheet ID

Your spreadsheet ID is in the URL of your Google Sheet:

```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
```

Copy the long string between `/d/` and `/edit` - that's your spreadsheet ID.

**Important:** Make sure your spreadsheet is set to "Anyone with the link can view" so the API key can access it.

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values
# GOOGLE_API_KEY=your_actual_google_api_key
# SPREADSHEET_ID=your_actual_spreadsheet_id
# GEMINI_MODEL=gemini-2.0-flash-exp
```

## Google Sheets Structure

Your spreadsheet should have the following structure:

### Food Sheets

**Food sheets** (any name except "config" or "sheet-context")

Each food sheet should have the following columns:

| Name | Details | Style | Reference (optional) |
|------|---------|-------|---------------------|
| Chicken breast | 2 lbs, fresh | Universal | |
| Ground beef tacos | 1 lb ground beef with taco spices | Mexican | Joy of Cooking p. 234 |
| Tofu stir-fry base | 1 block extra firm tofu | Flexible | |

**Column descriptions:**
- **Name**: The name of the dish or component
- **Details**: Things you want the AI to know about this dish (quantity, prep state, etc.)
- **Style**: Can be:
  - A cuisine style (e.g., "Mexican", "Italian", "Thai")
  - "Flexible" - the AI can modify this component to fit the meal style
  - "Universal" - this ingredient works with multiple (but not all) styles
- **Reference** (optional): Cookbook page reference (e.g., "Joy of Cooking p. 234")

### Optional Sheets

**"config" sheet**
| key | value |
|-----|-------|
| prompt_header | Give me meal suggestions based on the following ingredients: |
| prompt_footer | Please suggest 5 diverse meals I can make with these ingredients. |

All config keys are optional.

**"sheet-context" sheet**
| sheet_name | context |
|------------|---------|
| Proteins | Here are the proteins I have available: |
| Vegetables | Fresh vegetables in my fridge: |

## Usage

```bash
# Make sure your virtual environment is activated
source .venv/bin/activate

# Run the app
python main.py

# Use a different .env file
python main.py --env-file /path/to/.env
```

The meal plan will be printed to your terminal.

## Example Output

```markdown
# Meal Plan

## Shopping

- 2 lbs chicken breast
- 1 lb ground beef
- Taco shells and toppings

## Pre-Prep

- Marinate chicken overnight
- Prep taco seasoning mix

## Day 1

### Dinner: Chicken Stir-Fry (Asian)

- Chicken breast (Joy of Cooking p. 234)
- Broccoli
- Carrots
- Rice

*Marinate chicken in soy sauce before cooking.*
```

## Troubleshooting

**"Failed to get sheet names" error:**
- Check that your GOOGLE_API_KEY is correct
- Verify your SPREADSHEET_ID is correct
- Make sure the spreadsheet sharing is set to "Anyone with the link can view"

**"Gemini API error" messages:**
- Check that your GOOGLE_API_KEY is valid and has access to Gemini API
- Verify the GEMINI_MODEL you specified exists (e.g., "gemini-2.0-flash-exp", "gemini-1.5-pro")

## Project Structure

```
lunchlady/
├── config.py           # Environment variable management
├── sheets_client.py    # Google Sheets API client
├── sheet_loader.py     # Data loading orchestration
├── prompt_builder.py   # Prompt assembly and formatting
├── gemini_client.py    # Gemini API client
├── main.py            # CLI entry point
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variable template
└── README.md          # This file
```

## License

MIT

## AI Disclosure

I wrote exactly none of this code.  Blame Sonnet 4.5 if there are bugs.

