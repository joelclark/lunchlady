"""OpenAI client for Lunch Lady."""

from typing import Optional
from openai import OpenAI, OpenAIError


class OpenAIClientError(Exception):
    """Raised when there's an error calling the OpenAI API."""
    pass


class OpenAIClient:
    """Client for generating meal plans using OpenAI."""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo")
            temperature: Sampling temperature (optional)
            max_tokens: Maximum tokens in response (optional)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate_meal_plan(self, prompt: str) -> str:
        """
        Generate a meal plan using the OpenAI API.

        Args:
            prompt: The prompt text to send to OpenAI

        Returns:
            The generated meal plan text.

        Raises:
            OpenAIClientError: If the API call fails
        """
        try:
            # Build request parameters
            params = {
                'model': self.model,
                'messages': [
                    {'role': 'user', 'content': prompt}
                ]
            }

            # Add optional parameters
            if self.temperature is not None:
                params['temperature'] = self.temperature

            if self.max_tokens is not None:
                params['max_tokens'] = self.max_tokens

            # Make API call
            response = self.client.chat.completions.create(**params)

            # Extract response text
            return response.choices[0].message.content

        except OpenAIError as e:
            raise OpenAIClientError(f"OpenAI API error: {e}")
        except Exception as e:
            raise OpenAIClientError(f"Unexpected error calling OpenAI: {e}")