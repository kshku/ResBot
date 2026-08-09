from pathlib import Path

import pymupdf
import pytest

RESUME_TYP_CONTENT = (
    "# Alice Doe\n\n## Experience\n\nSenior Python developer at Acme Corp.\n"
)
JD_MD_CONTENT = "# Software Engineer\n\nWe need someone strong in Python and FastAPI.\n"
JD_TXT_CONTENT = "Software Engineer role. Python, FastAPI, and Docker experience required.\n"
PDF_PAGE_TEXTS = ["Alice Doe resume page one.\n", "Alice Doe resume page two.\n"]


@pytest.fixture
def sample_files(tmp_path: Path):
    resume_typ = tmp_path / "resume.typ"
    resume_typ.write_text(RESUME_TYP_CONTENT)

    jd_md = tmp_path / "jd.md"
    jd_md.write_text(JD_MD_CONTENT)

    jd_txt = tmp_path / "jd.txt"
    jd_txt.write_text(JD_TXT_CONTENT)

    return resume_typ, jd_md, jd_txt


@pytest.fixture
def resume_pdf(tmp_path: Path) -> Path:
    path = tmp_path / "resume.pdf"
    doc = pymupdf.open()
    for text in PDF_PAGE_TEXTS:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()
    return path
