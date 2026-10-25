import time

from selenium.webdriver.remote.webdriver import WebDriver

from config import settings


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)
        self.wait_for_document_ready()

    def wait_for_document_ready(self, timeout: int = 30) -> None:
        end = time.time() + timeout
        while time.time() < end:
            if self.driver.execute_script("return document.readyState") == "complete":
                return
            time.sleep(0.2)

    def page_height(self) -> int:
        return self.driver.execute_script(
            "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);"
        )

    def scroll_position(self) -> int:
        return self.driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")

    def scroll_to_top(self) -> None:
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_by(self, pixels: int) -> None:
        self.driver.execute_script("window.scrollBy(0, arguments[0]);", pixels)
        time.sleep(settings.SCROLL_PAUSE)

    def scroll_into_view(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center', inline:'nearest'});", element)
        time.sleep(settings.SCROLL_PAUSE)

    def is_in_viewport(self, element) -> bool:
        return bool(self.driver.execute_script(
            """
            const r = arguments[0].getBoundingClientRect();
            return r.width > 0 && r.height > 0 && r.bottom > 0 && r.right > 0 &&
                   r.top < (window.innerHeight || document.documentElement.clientHeight) &&
                   r.left < (window.innerWidth || document.documentElement.clientWidth);
            """, element))

    def computed_style_visible(self, element) -> bool:
        """display != none, visibility != hidden, opacity > 0 (is_displayed() already covers most of this)."""
        return bool(self.driver.execute_script(
            """
            const s = window.getComputedStyle(arguments[0]);
            return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0;
            """, element))
