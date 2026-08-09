
import pytest
from conftest import (
    JD_MD_CONTENT,
    JD_TXT_CONTENT,
    PDF_PAGE_TEXTS,
    RESUME_TYP_CONTENT,
)

from resbot.loader.loader import load_jd, load_resume
from resbot.loader.text_loader import TextFileLoader


def test_text_loader_reads_content_and_metadata(sample_files):
    resume_typ, _, _ = sample_files

    docs = TextFileLoader(resume_typ).load()

    assert len(docs) == 1
    doc = docs[0]
    assert doc.page_content == RESUME_TYP_CONTENT
    assert doc.metadata["source"] == str(resume_typ)
    assert doc.metadata["filetype"] == "typst"


def test_text_loader_strips_bom(tmp_path):
    path = tmp_path / "bom.txt"
    path.write_text("hello\n", encoding="utf-8-sig")

    doc = TextFileLoader(path).load()[0]

    assert not doc.page_content.startswith("\ufeff")
    assert doc.page_content == "hello\n"


def test_load_resume_typ(sample_files):
    resume_typ, _, _ = sample_files

    docs = load_resume(resume_typ)

    assert len(docs) == 1
    assert docs[0].page_content == RESUME_TYP_CONTENT
    assert docs[0].metadata["filetype"] == "typst"


def test_load_resume_pdf_yields_one_document_per_page(resume_pdf):
    docs = load_resume(resume_pdf)

    assert len(docs) == 2
    assert [d.metadata["page"] for d in docs] == [0, 1]
    assert docs[0].page_content.strip() == PDF_PAGE_TEXTS[0].strip()
    assert all(d.metadata["filetype"] == "pdf" for d in docs)
    assert all(d.metadata["source"] == str(resume_pdf) for d in docs)


def test_load_jd_markdown(sample_files):
    _, jd_md, _ = sample_files

    docs = load_jd(jd_md)

    assert len(docs) == 1
    assert docs[0].page_content == JD_MD_CONTENT
    assert docs[0].metadata["filetype"] == "markdown"


def test_load_jd_txt(sample_files):
    _, _, jd_txt = sample_files

    docs = load_jd(jd_txt)

    assert len(docs) == 1
    assert docs[0].page_content == JD_TXT_CONTENT
    assert docs[0].metadata["filetype"] == "text"


def test_load_jd_pdf(resume_pdf):
    docs = load_jd(resume_pdf)

    assert len(docs) == 2
    assert all(d.metadata["filetype"] == "pdf" for d in docs)


@pytest.mark.parametrize("loader", [load_resume, load_jd])
@pytest.mark.parametrize("suffix", [".docx", ".html", ".png"])
def test_unsupported_extension_raises(loader, tmp_path, suffix):
    path = tmp_path / f"file{suffix}"
    path.write_text("x")

    with pytest.raises(ValueError, match="unsupported"):
        loader(path)


def test_nonexistent_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_resume(tmp_path / "missing.typ")
