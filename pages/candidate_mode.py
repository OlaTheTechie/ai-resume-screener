import streamlit as st
from utils.text_extraction import extract_text_from_file
from utils.similarity import get_similarity_score
from utils.preprocessing import preprocess_text

def score_badge(score: float) -> str:
    """Return color-coded badge for score quality."""
    if score >= 0.85:
        color, label = 'green', 'Excellent Match'
    elif score >= 0.7:
        color, label = 'yellow', 'Good Match'
    elif score >= 0.5:
        color, label = 'orange', 'Fair Match'
    else:
        color, label = 'red', 'Weak Match'
    return f'<span style="color: {color}; font-weight: bold;">{label}</span>'

def candidate_mode():
    st.title("Candidate Mode - Resume Match Checker")
    st.markdown("Compare your resume with a job description to see how well they match.")

    # Resume input
    st.subheader("Resume")
    resume_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="resume_file")
    resume_text_input = st.text_area("Or paste your resume text here", height=200, key="resume_text_input")

    # JD input
    st.subheader("Job Description")
    jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'], key="jd_file")
    jd_text_input = st.text_area("Or paste the job description text here", height=200, key="jd_text_input")

    resume_text = ""
    jd_text = ""

    # Extract resume text from file or use pasted text
    if resume_file is not None:
        resume_text = extract_text_from_file(resume_file)
    elif resume_text_input.strip():
        resume_text = resume_text_input.strip()

    # Extract JD text from file or use pasted text
    if jd_file is not None:
        jd_text = extract_text_from_file(jd_file)
    elif jd_text_input.strip():
        jd_text = jd_text_input.strip()

    if st.button("Check Similarity"):
        if not resume_text or not jd_text:
            st.warning("Please provide both resume and job description.")
        else:
            # Preprocess
            resume_clean = preprocess_text(resume_text)
            jd_clean = preprocess_text(jd_text)

            # Get score
            score = get_similarity_score(resume_clean, jd_clean)

            st.markdown("### Result Summary")
            st.markdown(f"**Similarity Score:** `{score:.2f}` (1.0 means perfect match)")
            st.markdown(f"**Match Rating:** {score_badge(score)}", unsafe_allow_html=True)

            # Interpretation guide
            st.info(
                """
                **Score Interpretation**:
                - **0.85 - 1.0**: Excellent alignment — your resume fits very well.
                - **0.70 - 0.85**: Good match — mostly relevant.
                - **0.50 - 0.70**: Fair match — consider improving keyword relevance.
                - **Below 0.50**: Weak match — significant differences from the job description.
                """
            )

            # Optional: show text snippet diff (simple approach)
            st.markdown("### Text Preview")
            with st.expander("Show resume and JD text preview"):
                st.text_area("Resume (processed)", resume_clean, height=150)
                st.text_area("Job Description (processed)", jd_clean, height=150)

if __name__ == "__main__":
    candidate_mode()
