from langchain_core.language_models.chat_models import BaseChatModel

from resbot.graph.state import AgentState
from resbot.loader.loader import load_jd, load_resume
from resbot.models.resume import ResumeAnalysis
from resbot.prompts.analysis import ANALYSIS_PROMPT


def load_docs(state: AgentState) -> dict:
    resume_docs = load_resume(state["resume_path"])
    jd_docs = load_jd(state["jd_path"])
    return {
        "resume_docs": resume_docs,
        "jd_docs": jd_docs,
    }

def extract_docs(state: AgentState) -> dict:
    resume_text = "\n\n".join(doc.page_content for doc in state["resume_docs"])
    jd_text = "\n\n".join(doc.page_content for doc in state["jd_docs"])
    return {
        "resume_text": resume_text,
        "jd_text": jd_text,
    }


def build_analyze_node(llm: BaseChatModel):
    structured_llm = llm.with_structured_output(ResumeAnalysis)

    def analyze(state: AgentState) -> dict:
        messages = ANALYSIS_PROMPT.format_messages(
            resume_text=state["resume_text"],
            jd_text=state["jd_text"],
        )
        return {"analysis": structured_llm.invoke(messages)}

    return analyze

