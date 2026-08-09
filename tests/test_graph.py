from conftest import JD_MD_CONTENT, RESUME_TYP_CONTENT, make_analysis

from resbot.graph.nodes import build_analyze_node, extract_docs, load_docs
from resbot.graph.workflow import build_agent_graph


class FakeStructuredOutput:
    def __init__(self, result):
        self.result = result
        self.messages = None

    def invoke(self, messages):
        self.messages = messages
        return self.result


class FakeLLM:
    def __init__(self, result):
        self.result = result
        self.structured_llm = None

    def with_structured_output(self, schema):
        self.structured_llm = FakeStructuredOutput(self.result)
        return self.structured_llm


def test_load_docs_reads_both_files(sample_files):
    resume_typ, jd_md, _ = sample_files

    result = load_docs({"resume_path": resume_typ, "jd_path": jd_md})

    assert len(result["resume_docs"]) == 1
    assert result["resume_docs"][0].page_content == RESUME_TYP_CONTENT
    assert len(result["jd_docs"]) == 1
    assert result["jd_docs"][0].page_content == JD_MD_CONTENT


def test_extract_docs_joins_page_content(sample_files):
    resume_typ, jd_md, _ = sample_files
    loaded = load_docs({"resume_path": resume_typ, "jd_path": jd_md})

    result = extract_docs(loaded)

    assert result["resume_text"] == RESUME_TYP_CONTENT
    assert result["jd_text"] == JD_MD_CONTENT


def test_analyze_node_returns_analysis():
    expected = make_analysis()
    analyze = build_analyze_node(FakeLLM(expected))

    result = analyze({"resume_text": "x", "jd_text": "y"})

    assert result["analysis"] == expected


def test_analyze_node_formats_both_texts_into_prompt():
    fake = FakeLLM(make_analysis())
    analyze = build_analyze_node(fake)

    analyze({"resume_text": "MY RESUME", "jd_text": "MY JD"})

    rendered = "\n".join(m.content for m in fake.structured_llm.messages)
    assert "MY RESUME" in rendered
    assert "MY JD" in rendered


def test_graph_runs_end_to_end(sample_files):
    resume_typ, jd_md, _ = sample_files
    expected = make_analysis()

    graph = build_agent_graph(FakeLLM(expected))
    result = graph.invoke({"resume_path": resume_typ, "jd_path": jd_md})

    assert result["analysis"] == expected
    assert result["resume_text"] == RESUME_TYP_CONTENT
    assert result["jd_text"] == JD_MD_CONTENT
