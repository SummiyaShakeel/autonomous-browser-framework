import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    WIDTH = int(os.getenv("WIDTH", 1280))
    HEIGHT = int(os.getenv("HEIGHT", 720))
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 30000))
    DEFAULT_URL = os.getenv("DEFAULT_URL", "https://google.com")
