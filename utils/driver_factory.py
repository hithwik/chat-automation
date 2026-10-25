from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import settings


def create_driver() -> webdriver.Remote:
    """Create a WebDriver. Selenium Manager (built into Selenium 4.6+) downloads the matching driver automatically."""
    width, height = settings.WINDOW_SIZE.split(",")
    browser = settings.BROWSER

    if browser == "chrome":
        opts = ChromeOptions()
        if settings.HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument(f"--window-size={width},{height}")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=opts)
    elif browser == "firefox":
        opts = FirefoxOptions()
        if settings.HEADLESS:
            opts.add_argument("-headless")
        opts.add_argument(f"--width={width}")
        opts.add_argument(f"--height={height}")
        driver = webdriver.Firefox(options=opts)
    elif browser == "edge":
        opts = EdgeOptions()
        if settings.HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument(f"--window-size={width},{height}")
        driver = webdriver.Edge(options=opts)
    else:
        raise ValueError(f"Unsupported BROWSER '{browser}'. Use chrome, firefox or edge.")

    driver.set_page_load_timeout(settings.PAGE_LOAD_TIMEOUT)
    return driver
