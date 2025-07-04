from flask import Flask, request, render_template_string
from matcher import extract_text_from_pdf, get_analysis
import tempfile

app = Flask(__name__)

# Load HTML and CSS content
with open("index.html", "r", encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()
with open("style.css", "r", encoding="utf-8") as f:
    STYLE = f"<style>{f.read()}</style>"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    jd_text = ""
    resume_filename = ""

    if request.method == "POST":
        jd_text = request.form.get("jd_text", "")
        resume_file = request.files.get("resume")

        if resume_file and resume_file.filename.endswith(".pdf"):
            resume_filename = resume_file.filename
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                resume_file.save(temp.name)
                resume_text = extract_text_from_pdf(temp.name)
                result = get_analysis(resume_text, jd_text)

    return render_template_string(
    STYLE + HTML_TEMPLATE,
    result=result,
    jd_text=jd_text,
    resume_filename=resume_filename
)

if __name__ == "__main__":
    app.run(debug=True)