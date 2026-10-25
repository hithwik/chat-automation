import re
from datetime import datetime

import pytest

from config import settings
from utils.driver_factory import create_driver
from utils.logger import get_logger
from utils.url_reader import read_urls

log = get_logger("conftest")


def pytest_generate_tests(metafunc):
    """Parametrize every test that asks for `url` using the URLs in the file."""
    if "url" in metafunc.fixturenames:
        urls = read_urls(settings.URL_FILE)
        metafunc.parametrize("url", urls, ids=urls)


@pytest.fixture
def driver():
    drv = create_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # Screenshot on failure
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            settings.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            name = re.sub(r"[^A-Za-z0-9]+", "_", item.name)[:80]
            path = settings.SCREENSHOT_DIR / f"{name}_{datetime.now():%Y%m%d_%H%M%S}.png"
            try:
                drv.save_screenshot(str(path))
                log.info("Screenshot saved: %s", path)
            except Exception as exc:  # noqa: BLE001
                log.warning("Could not take screenshot: %s", exc)
