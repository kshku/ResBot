from collections.abc import Iterator
from pathlib import Path
from typing import ClassVar

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class TextFileLoader(BaseLoader):
    """Reads a text file as a single document."""

    filetype_map: ClassVar[dict[str, str]] = {
        ".typ": "Typst",
        ".md": "Markdown",
        ".txt": "Text file",
    }

    def __init__(self, path: Path, encoding="utf-8-sig"):
        self.path = path
        self.encoding = encoding

    def lazy_load(self) -> Iterator[Document]:
        yield Document(
            page_content=self.path.read_text(encoding=self.encoding),
            metadata={"source": str(self.path), "filetype": self.filetype_map[self.path.suffix]},
        )

def load_text_file(path: Path):
    return TextFileLoader(path).load()
