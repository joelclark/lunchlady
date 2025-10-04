"""Configuration management for Lunch Lady."""

import os
import sys
from pathlib import Path
from typing import Optional


class ConfigError(Exception):
    """Raised when configuration is invalid or incomplete."""
    pass


class Config:
    """Manages application configuration from environment variables."""

    REQUIRED_VARS = [
        'GOOGLE_API_KEY',
        'SPREADSHEET_ID',
        'GEMINI_MODEL'
    ]

    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            env_file: Path to .env file. Defaults to '.env' in current directory.
        """
        self._load_env_file(env_file or '.env')
        self._validate()

    def _load_env_file(self, path: str) -> None:
        """Load environment variables from .env file."""
        env_path = Path(path)

        if not env_path.exists():
            raise ConfigError(f"Environment file not found: {path}")

        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                # Parse key=value
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    os.environ[key] = value

    def _validate(self) -> None:
        """Validate that all required environment variables are set."""
        missing = []
        for var in self.REQUIRED_VARS:
            if not os.environ.get(var):
                missing.append(var)

        if missing:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get configuration value."""
        return os.environ.get(key, default)

    @property
    def google_api_key(self) -> str:
        """Google API key (used for both Sheets and Gemini)."""
        return os.environ['GOOGLE_API_KEY']

    @property
    def spreadsheet_id(self) -> str:
        """Google Sheets spreadsheet ID."""
        return os.environ['SPREADSHEET_ID']

    @property
    def gemini_model(self) -> str:
        """Gemini model name."""
        return os.environ['GEMINI_MODEL']

    @property
    def gemini_temperature(self) -> Optional[float]:
        """Gemini temperature parameter."""
        temp = self.get('GEMINI_TEMPERATURE')
        return float(temp) if temp else None

    @property
    def gemini_max_tokens(self) -> Optional[int]:
        """Gemini max tokens parameter."""
        tokens = self.get('GEMINI_MAX_TOKENS')
        return int(tokens) if tokens else None