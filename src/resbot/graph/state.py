from pathlib import Path
from typing import TypedDict

from langchain_core.documents import Document

from resbot.models.resume import ResumeAnalysis


class AgentState(TypedDict, total=False):
    resume_path: Path
    jd_path: Path

    resume_docs: list[Document]
    jd_docs: list[Document]

    resume_text: str
    jd_text: str

    analysis: ResumeAnalysis | None
