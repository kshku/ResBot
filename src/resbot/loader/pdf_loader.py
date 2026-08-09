from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader


class PDFLoader(PyMuPDF4LLMLoader):
    """Reads a PDF file into Documents, adds filetype metadata."""

    def __init__(self, path: Path):
        super().__init__(str(path))

# PyMuPDF4LLMLoader is actually overriding the load() function,
# but langchain docs says not to therefore using a wrapper function
# to add filetype metadata
def load_pdf(path: Path):
    docs = PDFLoader(path).load()
    for doc in docs:
        doc.metadata["filetype"] = "PDF"
    return docs

