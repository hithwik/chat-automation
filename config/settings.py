"""Central configuration. Override any value with an environment variable."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

URL_FILE = Path(os.getenv("URL_FILE", BASE_DIR / "data" / "urls.txt"))
SCREENSHOT_DIR = BASE_DIR / "reports" / "screenshots"

BROWSER = os.getenv("BROWSER", "chrome").lower()          # chrome | firefox | edge
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")

PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))
ELEMENT_WAIT_TIMEOUT = int(os.getenv("ELEMENT_WAIT_TIMEOUT", "20"))   # seconds to hunt for the button
SCROLL_STEP_PX = int(os.getenv("SCROLL_STEP_PX", "600"))
SCROLL_PAUSE = float(os.getenv("SCROLL_PAUSE", "0.4"))               # pause after each scroll (lazy-load)

POST_LOAD_WAIT = int(os.getenv("POST_LOAD_WAIT", "10"))   # seconds to wait after the page opens

# Locator under test
QUICK_LAUNCHER_ID = "header-logged-in-midbar"
