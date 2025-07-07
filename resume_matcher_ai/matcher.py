from PyPDF2 import PdfReader
from langchain_groq.chat_models import ChatGroq
from langchain_core.messages import HumanMessage

# Replace with your real key

import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.0,
    max_tokens=512,
    api_key=GROQ_API_KEY,
)

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def create_prompt(resume_text, jd_text):
    return f"""
You are an AI Resume Matcher analyzing a candidate's resume against a job description.

You must:
- Read and understand both the resume and JD.
- Identify the candidate's name, graduation year.
- Calculate:
  - Full-time experience (in months and years)
  - Internship experience (in months and years)
- Extract key **matched skills** and **missing skills**
- Give a **Fit Score** out of 100
- Show a **one-line hiring recommendation** based on fit score also for consideration
(e.g., - ✅ shortlisted
  - ⚠️ Partially Fit
  - ❌ Rejected)

Now format your output exactly like this (markdown styled). **Do not add any summary or explanation outside this format**:


👤 Name:** <Full Name>  

📊 Fit Score:** <score>%  
✅ Recommendation:** <one-line decision>

💼 Full-Time Experience:** <months> months (<years> years)  
💼 Internship Experience:** <months> months (<years> years)  

⚠️ Missing Skills:**  
<comma-separated list or bullet points of missing/required skills>  

---

Resume:
\"\"\"{resume_text}\"\"\"

Job Description:
\"\"\"{jd_text}\"\"\"
"""


def get_analysis(resume_text, jd_text):
    prompt = create_prompt(resume_text, jd_text)
    message = [HumanMessage(content=prompt)]
    response = llm(message)
    return response.content
