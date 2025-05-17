import streamlit as st
from utils.text_extraction import extract_text_from_file
from utils.similarity import get_similarity_score
from utils.preprocessing import preprocess_text

def score_badge(score: float) -> str:
    """Return color-coded badge for score quality."""
    if score >= 0.85:
        color = 'green'
        label = 'Excellent'
    elif score >= 0.7:
        color = 'yellow'
        label = 'Good'
    elif score >= 0.5:
        color = 'orange'
        label = 'Fair'
    else:
        color = 'red'
        label = 'Poor'
    return f'<span style="color: {color}; font-weight: bold;">{label}</span>'

def manager_mode():
    st.title("Manager Mode - Bulk Resume Screening")

    st.markdown("Upload multiple resumes or paste them below (one per box):")
    resumes = st.file_uploader(
        "Upload Resumes (PDF, DOCX, TXT) - multiple allowed",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        key="manager_resumes"
    )

    pasted_resumes_input = st.text_area(
        "Or paste multiple resumes separated by '---' (three dashes on a new line):",
        height=200,
        key="pasted_resumes"
    )

    st.markdown("Upload Job Description or paste it below:")
    jd_file = st.file_uploader(
        "Upload Job Description (PDF, DOCX, TXT)",
        type=['pdf', 'docx', 'txt'],
        key="manager_jd_file"
    )
    jd_text_input = st.text_area(
        "Or paste job description text here:",
        height=150,
        key="manager_jd_text"
    )

    # Extract JD text
    jd_text = ""
    if jd_file is not None:
        jd_text = extract_text_from_file(jd_file)
    elif jd_text_input.strip():
        jd_text = jd_text_input.strip()

    # Prepare resume texts list
    resume_texts = []

    if resumes:
        for resume in resumes:
            text = extract_text_from_file(resume)
            if text.strip():
                resume_texts.append((resume.name, text))

    if pasted_resumes_input.strip():
        raw_resumes = [r.strip() for r in pasted_resumes_input.split('---') if r.strip()]
        for i, text in enumerate(raw_resumes, start=1):
            resume_texts.append((f"Pasted Resume {i}", text))

    if st.button("Screen Resumes"):
        if not resume_texts:
            st.warning("Please provide at least one resume (uploaded or pasted).")
            return
        if not jd_text.strip():
            st.warning("Please provide a job description (uploaded or pasted).")
            return

        jd_text_clean = preprocess_text(jd_text)
        scores = []
        for name, text in resume_texts:
            resume_text_clean = preprocess_text(text)
            score = get_similarity_score(resume_text_clean, jd_text_clean)
            scores.append((name, score))

        # Sort descending by score
        scores.sort(key=lambda x: x[1], reverse=True)

        st.header("Candidate Ranking:")

        # Display summary stats
        scores_only = [s for _, s in scores]
        st.markdown(f"**Total Candidates:** {len(scores)}")
        st.markdown(f"**Top Score:** {max(scores_only):.2f}")
        st.markdown(f"**Average Score:** {sum(scores_only)/len(scores_only):.2f}")

        # Display table with scores and badges
        st.markdown(
            """
            <style>
            .score-table th, .score-table td {
                padding: 8px 12px;
                text-align: left;
            }
            </style>
            """, unsafe_allow_html=True
        )

        st.markdown("<table class='score-table'>", unsafe_allow_html=True)
        st.markdown("<tr><th>Candidate</th><th>Similarity Score</th><th>Rating</th></tr>", unsafe_allow_html=True)
        for name, score in scores:
            badge_html = score_badge(score)
            st.markdown(f"<tr><td>{name}</td><td>{score:.2f}</td><td>{badge_html}</td></tr>", unsafe_allow_html=True)
        st.markdown("</table>", unsafe_allow_html=True)
