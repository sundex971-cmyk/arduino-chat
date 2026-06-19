from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True)
class DocumentSource:
    """A single documentation page to download.

    Attributes:
        category:    Top-level folder inside data/docs/ (e.g. "arduino").
        section:     Sub-folder / tag within that category (e.g. "language-reference").
        page_url:    Human-readable URL shown as metadata in the saved file.
        raw_base_url: Root URL of the raw file host (GitHub raw, etc.).
        source_path: Path to the file relative to raw_base_url.
    """

    category: str
    section: str
    page_url: str
    raw_base_url: str
    source_path: str

    @property
    def raw_url(self) -> str:
        return f"{self.raw_base_url}/{quote(self.source_path)}"