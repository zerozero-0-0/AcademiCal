import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env early
load_dotenv()

# Discord bot tokens and channels
DISCORD_TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
CHANNEL_ID: Optional[str] = os.getenv("CHANNEL_ID")  # Keep as str; cast at use-site

# Daily due prompt schedule (default 21:00). Overridable with env vars.
DAILY_DUE_PROMPT_HOUR: int = int(os.getenv("DAILY_DUE_PROMPT_HOUR", "21"))
DAILY_DUE_PROMPT_MINUTE: int = int(os.getenv("DAILY_DUE_PROMPT_MINUTE", "00"))

# Application timezone (IANA tz database name). Default: Asia/Tokyo
APP_TZ: str = os.getenv("APP_TZ", "Asia/Tokyo")
