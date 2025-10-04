"""FastAPI web interface for Lunch Lady."""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from config import Config, ConfigError
from sheets_client import SheetsClientError
from gemini_client import GeminiClientError
from meal_plan_generator import MealPlanGenerator


# Get script directory
SCRIPT_DIR = Path(__file__).parent

app = FastAPI(title="Lunch Lady", description="Meal Planning Service")


@app.get("/new", response_class=HTMLResponse)
async def generate_meal_plan():
    """
    Generate a new meal plan in HTML format.

    Returns:
        HTML response with the generated meal plan
    """
    try:
        # Load configuration from default .env file
        config = Config()

        # Generate meal plan with HTML output
        generator = MealPlanGenerator(config, SCRIPT_DIR)
        result = generator.generate(output_format='html')

        return result.response

    except ConfigError as e:
        raise HTTPException(status_code=500, detail=f"Configuration error: {e}")
    except SheetsClientError as e:
        raise HTTPException(status_code=500, detail=f"Google Sheets error: {e}")
    except GeminiClientError as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/")
async def root():
    """Root endpoint with basic info."""
    return {
        "name": "Lunch Lady",
        "description": "Meal Planning Service",
        "endpoints": {
            "/new": "Generate a new meal plan (HTML)"
        }
    }
