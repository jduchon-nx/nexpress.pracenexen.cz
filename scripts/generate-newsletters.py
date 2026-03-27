import json
import re
from pathlib import Path

NEWSLETTER_DIR = Path("newsletters")
OUTPUT_FILE = Path("newsletters.json")

PATTERN = re.compile(
    r"^nexpress-(?P<year>\d{4})-(?P<month>\d{2})(-(?P<day>\d{2}))?\.pdf$",
    re.IGNORECASE
)

def parse_file(pdf_path: Path):
    filename = pdf_path.name
    match = PATTERN.match(filename)

    if match:
        year = match.group("year")
        month = match.group("month")
        day = match.group("day") or "01"

        return {
            "title": "Nexpress",
            "date": f"{year}-{month}-{day}",
            "file": str(pdf_path).replace("\\", "/"),
        }

    # fallback if someone uploads a badly named file
    return {
        "title": "Nexpress",
        "date": "1970-01-01",
        "file": str(pdf_path).replace("\\", "/"),
    }

def main():
    if not NEWSLETTER_DIR.exists():
        OUTPUT_FILE.write_text("[]", encoding="utf-8")
        return

    newsletters = [parse_file(pdf) for pdf in NEWSLETTER_DIR.glob("*.pdf")]

    newsletters.sort(key=lambda x: x["date"], reverse=True)

    OUTPUT_FILE.write_text(
        json.dumps(newsletters, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

if __name__ == "__main__":
    main()
