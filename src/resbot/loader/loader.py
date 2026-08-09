from pathlib import Path

from langchain_core.documents import Document

from .pdf_loader import load_pdf
from .text_loader import load_text_file


def load_resume(path: Path) -> list[Document]:
    match path.suffix:
        case ".pdf":
            return load_pdf(path)
        case ".typ":
            return load_text_file(path)
        case _:
            raise ValueError(f"unsupported resume format '{path.suffix}' (expected .pdf or .typ)")

def load_jd(path: Path) -> list[Document]:
    match path.suffix:
        case ".pdf":
            return load_pdf(path)
        case ".txt" | ".md":
            return load_text_file(path)
        case _:
            raise ValueError(f"unsupported JD format '{path.suffix}' (expected .pdf, .txt, or .md)")

