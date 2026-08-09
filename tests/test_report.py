from conftest import make_analysis

from resbot.report import format_analysis


def test_format_analysis_includes_score():
    text = format_analysis(make_analysis())

    assert "**Score: 82/100**" in text


def test_format_analysis_includes_all_sections():
    text = format_analysis(make_analysis())

    assert "## Summary" in text
    assert "Good overall match" in text
    assert "## Strengths" in text
    assert "- Python expertise" in text
    assert "- Leadership" in text
    assert "## Weaknesses" in text
    assert "- No cloud experience" in text
    assert "## Missing Keywords" in text
    assert "- Kubernetes" in text
    assert "## Suggestions" in text
    assert "- Add a projects section" in text
