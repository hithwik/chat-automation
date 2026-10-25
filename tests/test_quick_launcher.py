import pytest

from config import settings
from pages.quick_launcher_page import QuickLauncherPage
from utils.logger import get_logger

log = get_logger(__name__)


@pytest.mark.smoke
def test_m365_quick_launcher_exists_and_visible(driver, url):
    """Open each URL and verify the Microsoft 365 Quick Launcher (id=o365ql-fabbutton)
    exists in the DOM and is visible after scrolling through the page."""
    log.info("Opening %s", url)
    page = QuickLauncherPage(driver)
    page.open(url)

    result = page.check_quick_launcher(url)
    log.info("Result for %s -> %s", url, result.summary())

    assert result.exists, f"[{url}] Button #{settings.QUICK_LAUNCHER_ID} NOT found. {' '.join(result.notes)}"
    assert result.displayed, f"[{url}] Button exists but is NOT displayed. {' '.join(result.notes)}"
    assert result.in_viewport, f"[{url}] Button not in viewport. {' '.join(result.notes)}"
    assert result.style_visible, f"[{url}] Button hidden by CSS. {' '.join(result.notes)}"
