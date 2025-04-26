from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import streamlit as st

def generate_feedback_pdf(filename="interview_summary.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "AI Interview Summary Report")
    y -= 30
    c.setFont("Helvetica", 10)

    for i, entry in enumerate(st.session_state.chat_history):
        q = entry["question"][:100] if "question" in entry else "N/A"
        a = entry["answer"][:100] if "answer" in entry else "N/A"
        e = entry["evaluation"][:200] if "evaluation" in entry else "N/A"
        score = entry.get("score", "N/A")
        c.drawString(40, y, f"Q{i+1}: {q}")
        y -= 15
        c.drawString(40, y, f"Answer: {a}")
        y -= 15
        c.drawString(40, y, f"Score: {score} / 10")
        y -= 15
        c.drawString(40, y, f"Feedback: {e}")
        y -= 40
        if y < 50:
            c.showPage()
            y = height - 40

    c.save()
    with open(filename, "rb") as f:
        st.download_button("📄 Download Summary PDF", f, file_name="interview_summary.pdf")