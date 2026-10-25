import time
from dataclasses import dataclass, field
from typing import List, Optional

from selenium.webdriver.common.by import By

from config import settings
from pages.base_page import BasePage
from utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class QuickLauncherResult:
    url: str
    exists: bool = False          # present in the DOM
    displayed: bool = False       # Selenium is_displayed()
    in_viewport: bool = False     # actually on screen after scrolling to it
    style_visible: bool = False   # display/visibility/opacity OK
    found_at_scroll_y: Optional[int] = None
    page_height: int = 0
    notes: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.exists and self.displayed and self.in_viewport and self.style_visible

    def summary(self) -> str:
        return (f"exists={self.exists}, displayed={self.displayed}, in_viewport={self.in_viewport}, "
                f"style_visible={self.style_visible}, found_at_scroll_y={self.found_at_scroll_y}, "
                f"page_height={self.page_height}")


class QuickLauncherPage(BasePage):
    """Page object for the Microsoft 365 Quick Launcher floating button (id=o365ql-fabbutton)."""

    BUTTON = (By.ID, settings.QUICK_LAUNCHER_ID)

    def _find(self):
        els = self.driver.find_elements(*self.BUTTON)
        return els[0] if els else None

    def locate_while_scrolling(self) -> Optional[object]:
        """
        Look for the button at the top of the page, then scroll down step by step to the bottom
        (so lazy-loaded / late-injected widgets get a chance to appear). Keeps polling until
        ELEMENT_WAIT_TIMEOUT expires. Returns the element or None.
        """
        deadline = time.time() + settings.ELEMENT_WAIT_TIMEOUT
        self.scroll_to_top()

        while True:
            el = self._find()
            if el:
                return el

            # scroll one step down; if already at the bottom, go back to top and keep polling
            before = self.scroll_position()
            self.scroll_by(settings.SCROLL_STEP_PX)
            moved = self.scroll_position() != before
            if not moved:
                log.info("Reached page bottom without finding the button, waiting/rechecking...")
                time.sleep(1)
                if time.time() >= deadline:
                    return self._find()
                self.scroll_to_top()
            elif time.time() >= deadline:
                return self._find()

    def check_quick_launcher(self, url: str) -> QuickLauncherResult:
        result = QuickLauncherResult(url=url)
        element = self.locate_while_scrolling()
        result.page_height = self.page_height()

        if element is None:
            result.notes.append(f"Element id='{settings.QUICK_LAUNCHER_ID}' not found in DOM.")
            return result

        result.exists = True
        result.found_at_scroll_y = self.scroll_position()

        # Scroll it into view, then verify visibility from several angles
        self.scroll_into_view(element)
        result.displayed = element.is_displayed()
        result.in_viewport = self.is_in_viewport(element)
        result.style_visible = self.computed_style_visible(element)

        if not result.displayed:
            result.notes.append("Element exists but Selenium reports it NOT displayed.")
        if not result.in_viewport:
            result.notes.append("Element is not within the viewport even after scrolling to it.")
        if not result.style_visible:
            result.notes.append("Element hidden via CSS (display/visibility/opacity).")
        return result
