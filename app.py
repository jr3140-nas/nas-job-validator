import streamlit as st
from PyPDF2 import PdfReader
import tempfile
import os

def evaluate_packet(text: str):
    feedback = []
    score = 0

    if "Follow-Up" in text or "Work Request" in text:
        score += 1
    else:
        feedback.append("❌ Missing indication of WR conversion or Follow-Up origin.")

    if "planner notes" in text.lower() or "site visit" in text.lower():
        score += 1
    else:
        feedback.append("❌ No planner notes or site visit details found.")

    if all(stage in text for stage in ["Before Task", "Replace", "After Task"]):
        score += 1
    else:
        feedback.append("❌ Job not clearly segmented into Before/During/After stages.")

    if any(verb in text.lower() for verb in ["remove", "install", "drain", "verify", "test"]):
        score += 1
    else:
        feedback.append("❌ Minimal or missing task instructions for technician.")

    if "crew size" in text.lower() or "duration" in text.lower():
        score += 1
    else:
        feedback.append("❌ No crew size or labor duration listed.")

    if "tool" in text.lower() or "part" in text.lower():
        score += 1
    else:
        feedback.append("❌ Parts and tools not listed.")

    if any(term in text.lower() for term in ["loto", "ppe", "hazard", "permit"]):
        score += 1
    else:
        feedback.append("❌ Safety planning details missing (LOTO, PPE, etc.).")

    if len(text) > 500:
        score += 1
    else:
        feedback.append("❌ Job packet appears incomplete or too brief.")

    return score, feedback

st.set_page_config(page_title="Job Packet Validator", layout="centered")
st.title("📋 Corrective Job Packet Quality Validator")

uploaded_files = st.file_uploader("Upload one or more job packet PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown("---")
        st.subheader(f"Review for: `{uploaded_file.name}`")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        try:
            reader = PdfReader(tmp_path)
            full_text = "\n".join(page.extract_text() or "" for page in reader.pages)

            score, feedback = evaluate_packet(full_text)

            st.metric("Checklist Score", f"{score} / 8")
            if score >= 6:
                st.success("✅ Job packet is well planned.")
            elif score >= 4:
                st.warning("⚠️ Partial plan — improvements recommended.")
            else:
                st.error("❌ Poor plan — major gaps in planning.")

            st.markdown("### Feedback:")
            for item in feedback:
                st.write("-", item)

        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")
        finally:
            os.unlink(tmp_path)

    st.markdown("---")
