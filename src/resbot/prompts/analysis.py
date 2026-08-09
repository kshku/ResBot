from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are a resume analysis assistant. Your job is to compare a candidate's resume against a job description and produce an honest, actionable assessment.

Score the resume from 0 to 100, where:
- 90-100: excellent match, strong alignment with the role
- 70-89: good match, some gaps or missed opportunities
- 50-69: weak match, several important gaps
- 0-49: poor match, significant misalignment

Use the job description's stated requirements as the benchmark. Base your judgement only on the resume and job description provided. Do not invent skills or achievements that are not present in the resume.

Respond only with the structured analysis."""

HUMAN_TEMPLATE = """Here is the resume:

<resume>
{resume_text}
</resume>

Here is the job description:

<job_description>
{jd_text}
</job_description>

Analyze the resume against this job description."""

ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_TEMPLATE),
    ]
)
