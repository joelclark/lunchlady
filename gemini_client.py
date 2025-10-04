"""Gemini client for Lunch Lady."""

from typing import Optional
from google import genai
from google.genai import types


class GeminiClientError(Exception):
    """Raised when there's an error calling the Gemini API."""
    pass


class GeminiClient:
    """Client for generating meal plans using Google Gemini."""

    def __init__(
        self,
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize the Gemini client.

        Args:
            model: Model name (e.g., "gemini-2.0-flash-exp", "gemini-1.5-pro")
            temperature: Sampling temperature (optional)
            max_tokens: Maximum tokens in response (optional)
        """
        self.client = genai.Client()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate_meal_plan(self, prompt: str) -> str:
        """
        Generate a meal plan using the Gemini API.

        Args:
            prompt: The prompt text to send to Gemini

        Returns:
            The generated meal plan text.

        Raises:
            GeminiClientError: If the API call fails
        """
        try:
            # Build config parameters
            config = {}
            if self.temperature is not None:
                config['temperature'] = self.temperature
            if self.max_tokens is not None:
                config['max_output_tokens'] = self.max_tokens

            generation_config = types.GenerateContentConfig(**config) if config else None

            # Make API call
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=generation_config
            )

            # Extract response text
            return response.text

        except Exception as e:
            raise GeminiClientError(f"Gemini API error: {e}")
