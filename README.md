# M365 Quick Launcher – Selenium (Python + pytest) Framework

Checks that the Microsoft 365 Quick Launcher button (`id="o365ql-fabbutton"`) exists **and is visible**
on every URL listed in `data/urls.txt`. The page is scrolled step by step so lazy-loaded widgets are caught.

## Structure
```
config/settings.py          browser, timeouts, scroll settings (env-overridable)
data/urls.txt               URLs under test (one per line, # = comment)
pages/base_page.py          scroll / viewport / wait helpers
pages/quick_launcher_page.py page object + visibility logic
utils/                      driver factory, URL reader, logger
tests/test_quick_launcher.py  parametrized test (one test per URL)
conftest.py                 driver fixture, URL parametrization, screenshot on failure
reports/                    report.html + failure screenshots
```

## Setup & run
```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                                # headless Chrome, report in reports/report.html
```
Requires Chrome (or Firefox/Edge) installed. Selenium 4.6+ downloads the matching driver automatically.

## Options (environment variables)
| Variable | Default | Purpose |
|---|---|---|
| `HEADLESS` | `true` | `false` to watch the browser |
| `BROWSER` | `chrome` | `chrome`, `firefox`, `edge` |
| `URL_FILE` | `data/urls.txt` | alternative URL file |
| `ELEMENT_WAIT_TIMEOUT` | `20` | seconds to keep scrolling/looking for the button |
| `SCROLL_STEP_PX` / `SCROLL_PAUSE` | `600` / `0.4` | scroll step size / pause |

Example: `HEADLESS=false BROWSER=firefox pytest -k shop-plans`

## What "pass" means
All four must be true: in DOM, `is_displayed()`, inside viewport after scrolling to it, and not hidden by CSS.
