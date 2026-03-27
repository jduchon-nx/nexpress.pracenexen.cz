import json
import os
import re
from pathlib import Path

NEWSLETTER_DIR = Path("newsletters")
OUTPUT_FILE = Path("newsletters.json")

# Expected filename examples:
# newsletter-2026-03.pdf
# newsletter-2026-03-15.pdf
PATTERNS = [
    re.compile(r"^(?P<name>.+)-(?P<year>\d{4})-(?P<month>\d{2})\.pdf$", re.IGNORECASE),
    re.compile(r"^(?P<name>.+)-(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\.pdf$", re.IGNORECASE),
]

def humanize_name(name: str) -> str:
    name = name.replace("-", " ").replace("_", " ").strip()
    return " ".join(word.capitalize() for word in name.split())

def parse_file(pdf_path: Path):
    filename = pdf_path.name

    for pattern in PATTERNS:
        match = pattern.match(filename)
        if match:
            groups = match.groupdict()
            title_base = humanize_name(groups["name"])

            year = groups["year"]
            month = groups["month"]
            day = groups.get("day") or "01"

            return {
                "title": title_base,
                "date": f"{year}-{month}-{day}",
                "file": str(pdf_path).replace("\\", "/"),
            }

    # Fallback when filename doesn't match expected pattern
    return {
        "title": pdf_path.stem,
        "date": "1970-01-01",
        "file": str(pdf_path).replace("\\", "/"),
    }

def main():
    if not NEWSLETTER_DIR.exists():
        OUTPUT_FILE.write_text("[]", encoding="utf-8")
        return

    newsletters = []
    for pdf in NEWSLETTER_DIR.glob("*.pdf"):
        newsletters.append(parse_file(pdf))

    newsletters.sort(key=lambda x: x["date"], reverse=True)

    OUTPUT_FILE.write_text(
        json.dumps(newsletters, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
