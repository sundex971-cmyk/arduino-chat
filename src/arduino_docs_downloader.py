from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = "https://docs.arduino.cc"
DOCS_CONTENT_RAW = "https://raw.githubusercontent.com/arduino/docs-content/main"
REFERENCE_RAW = "https://raw.githubusercontent.com/arduino/reference-en/master"
SAVE_DIR = Path(__file__).resolve().parents[1] / "data" / "docs"
REQUEST_TIMEOUT = 20
HEADERS = {
    "User-Agent": "arduino-chat-doc-downloader/1.0",
}


@dataclass(frozen=True)
class DocumentSource:
    section: str
    page_url: str
    raw_base_url: str
    source_path: str

    @property
    def raw_url(self) -> str:
        return f"{self.raw_base_url}/{quote(self.source_path)}"


SOURCES = [
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language/functions/analog-io/analogwrite/",
        REFERENCE_RAW,
        "Language/Functions/Analog IO/analogWrite.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language/functions/analog-io/analogread/",
        REFERENCE_RAW,
        "Language/Functions/Analog IO/analogRead.adoc",
    ),
    DocumentSource(
        "getting-started",
        f"{BASE_URL}/learn/starting-guide/getting-started-arduino/",
        DOCS_CONTENT_RAW,
        "content/learn/01.starting-guide/00.getting-started-arduino/getting-started-arduino.md",
    ),
    DocumentSource(
        "getting-started",
        f"{BASE_URL}/learn/programming/sketches/",
        DOCS_CONTENT_RAW,
        "content/learn/03.programming/03.sketches/sketches.md",
    ),
    DocumentSource(
        "pins-and-io",
        f"{BASE_URL}/learn/microcontrollers/digital-pins/",
        DOCS_CONTENT_RAW,
        "content/learn/02.microcontrollers/01.digital-pins/digital-pins.md",
    ),
    DocumentSource(
        "pins-and-io",
        f"{BASE_URL}/learn/microcontrollers/analog-input/",
        DOCS_CONTENT_RAW,
        "content/learn/02.microcontrollers/02.analog-input/analog-input.md",
    ),
    DocumentSource(
        "pins-and-io",
        f"{BASE_URL}/learn/microcontrollers/analog-output/",
        DOCS_CONTENT_RAW,
        "content/learn/02.microcontrollers/03.analog-output/analog-output.md",
    ),
    DocumentSource(
        "programming-basics",
        f"{BASE_URL}/learn/programming/reference/",
        DOCS_CONTENT_RAW,
        "content/learn/03.programming/00.reference/reference.md",
    ),
    DocumentSource(
        "programming-basics",
        f"{BASE_URL}/learn/programming/variables/",
        DOCS_CONTENT_RAW,
        "content/learn/03.programming/01.variables/variables.md",
    ),
    DocumentSource(
        "programming-basics",
        f"{BASE_URL}/learn/programming/functions/",
        DOCS_CONTENT_RAW,
        "content/learn/03.programming/02.functions/functions.md",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/",
        DOCS_CONTENT_RAW,
        "content/programming/01.language-reference/language-reference.md",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/digital-io/pinMode/",
        REFERENCE_RAW,
        "Language/Functions/Digital IO/pinMode.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/digital-io/digitalread/",
        REFERENCE_RAW,
        "Language/Functions/Digital IO/digitalRead.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/digital-io/digitalwrite/",
        REFERENCE_RAW,
        "Language/Functions/Digital IO/digitalWrite.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/analog-io/analogRead/",
        REFERENCE_RAW,
        "Language/Functions/Analog IO/analogRead.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/analog-io/analogWrite/",
        REFERENCE_RAW,
        "Language/Functions/Analog IO/analogWrite.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/time/delay/",
        REFERENCE_RAW,
        "Language/Functions/Time/delay.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/time/millis/",
        REFERENCE_RAW,
        "Language/Functions/Time/millis.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/communication/serial/",
        REFERENCE_RAW,
        "Language/Functions/Communication/Serial.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/communication/serial/begin/",
        REFERENCE_RAW,
        "Language/Functions/Communication/Serial/begin.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/communication/serial/available/",
        REFERENCE_RAW,
        "Language/Functions/Communication/Serial/available.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/communication/serial/read/",
        REFERENCE_RAW,
        "Language/Functions/Communication/Serial/read.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/communication/serial/print/",
        REFERENCE_RAW,
        "Language/Functions/Communication/Serial/print.adoc",
    ),
    DocumentSource(
        "language-reference",
        f"{BASE_URL}/language-reference/en/functions/communication/serial/println/",
        REFERENCE_RAW,
        "Language/Functions/Communication/Serial/println.adoc",
    ),
]


def describe_http_error(error: HTTPError) -> str:
    message = f"HTTP {error.code}: {error.reason}"

    if error.code == 404:
        message += " (source file was not found)"
    elif error.code in {403, 429}:
        retry_after = error.headers.get("Retry-After")
        rate_limit_remaining = error.headers.get("X-RateLimit-Remaining")
        message += " (rate limit or access restriction)"

        if retry_after:
            message += f"; retry after {retry_after} seconds"
        if rate_limit_remaining is not None:
            message += f"; remaining requests: {rate_limit_remaining}"

    return message


def fetch_text(url: str) -> str | None:
    request = Request(url, headers=HEADERS)
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(encoding, errors="replace")
    except HTTPError as error:
        print(f"[ERROR] Failed to fetch {url}: {describe_http_error(error)}")
    except URLError as error:
        print(f"[ERROR] Failed to fetch {url}: {error.reason}")
    except TimeoutError:
        print(f"[ERROR] Failed to fetch {url}: request timed out")

    return None


def clean_text(text: str) -> str:
    lines = text.splitlines()
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def format_content(source: DocumentSource, content: str) -> str:
    return "\n".join(
        [
            f"Source page: {source.page_url}",
            f"Source file: {source.raw_url}",
            "",
            clean_text(content),
            "",
        ]
    )


def save_text(filename: str, content: str) -> bool:
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    path = SAVE_DIR / filename
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as error:
        print(f"[ERROR] Failed to save {path}: {error}")
        return False

    print(f"[OK] Saved: {path}")
    return True


def source_to_filename(source: DocumentSource) -> str:
    parsed = urlparse(source.page_url)
    path = parsed.path.strip("/").replace("/", "_")
    return f"{source.section}__{path}.txt"


def main():
    saved_count = 0
    skipped_count = 0

    for source in SOURCES:
        print(f"[INFO] Fetching: {source.page_url}")

        content = fetch_text(source.raw_url)
        if content is None:
            skipped_count += 1
            continue

        formatted_content = format_content(source, content)
        filename = source_to_filename(source)
        if save_text(filename, formatted_content):
            saved_count += 1
        else:
            skipped_count += 1

    print(f"[DONE] Saved: {saved_count}; skipped: {skipped_count}")


if __name__ == "__main__":
    main()
