from resbot.models.resume import ResumeAnalysis


def format_analysis(analysis: ResumeAnalysis) -> str:
    lines = [
        "# Resume Analysis",
        "",
        f"**Score: {analysis.score}/100**",
        "",
        "## Summary",
        analysis.summary,
        "",
        "## Strengths",
    ]
    lines += [f"- {item}" for item in analysis.strengths]
    lines += ["", "## Weaknesses"]
    lines += [f"- {item}" for item in analysis.weaknesses]
    lines += ["", "## Missing Keywords"]
    lines += [f"- {item}" for item in analysis.missing_keywords]
    lines += ["", "## Suggestions"]
    lines += [f"- {item}" for item in analysis.suggestions]
    return "\n".join(lines) + "\n"
