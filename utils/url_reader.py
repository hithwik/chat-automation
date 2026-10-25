from pathlib import Path
from typing import List

from utils.logger import get_logger

log = get_logger(__name__)


def read_urls(file_path: Path) -> List[str]:
    """Read URLs from a text file (one per line). Skips blanks/comments, removes duplicates, keeps order."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"URL file not found: {path}")

    urls, seen = [], set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.lower().startswith(("http://", "https://")):
            log.warning("Skipping invalid URL (must start with http/https): %s", line)
            continue
        if line not in seen:
            seen.add(line)
            urls.append(line)

    if not urls:
        raise ValueError(f"No valid URLs found in {path}")
    log.info("Loaded %d URL(s) from %s", len(urls), path)
    return urls
