from pydantic import BaseModel


class ResumeAnalysis(BaseModel):
    score: int
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    missing_keywords: list[str]
    suggestions: list[str]
