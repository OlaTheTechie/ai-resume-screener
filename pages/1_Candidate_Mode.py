import streamlit as st
import sys
import os
from pathlib import Path

# adding parent directory to path (because I'm lazy)
sys.path.append(str(Path(__file__).parent.parent))

from utils.text_extraction import extract_text_from_file, preprocess_text
from utils.similarity import calculate_similarity, extract_keywords, compare_keywords

def main():
    st.title("Candidate Mode")
    st.markdown("""
    Upload your resume and a job description to get:
    - Match score
    - Keyword analysis
    - Improvement suggestions
    """)

    # file upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resume")
        resume_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt']
        )
    
    with col2:
        st.subheader("Job Description")
        job_desc_file = st.file_uploader(
            "Upload job description (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt']
        )
        job_desc_text = st.text_area(
            "Or paste job description here",
            height=200
        )

    if resume_file and (job_desc_file or job_desc_text):
        # processing resume
        resume_text = extract_text_from_file(resume_file)
        resume_text = preprocess_text(resume_text)
        
        # processing job description
        if job_desc_file:
            job_desc = extract_text_from_file(job_desc_file)
        else:
            job_desc = job_desc_text
        job_desc = preprocess_text(job_desc)
        
        # calculating match
        similarity_score = calculate_similarity(resume_text, job_desc)
        
        # keyword stuff
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_desc)
        keyword_comparison = compare_keywords(resume_keywords, job_keywords)
        
        # showing results
        st.markdown("---")
        st.subheader("Analysis Results")
        
        # match score
        st.metric(
            "Match Score",
            f"{similarity_score:.1%}",
            delta=None
        )
        
        # keyword analysis
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Matched Keywords")
            st.write(", ".join(keyword_comparison['matched']))
        
        with col2:
            st.subheader("Missing Keywords")
            st.write(", ".join(keyword_comparison['missing']))
        
        # tips
        st.subheader("Improvement Suggestions")
        if keyword_comparison['missing']:
            st.markdown("""
            Consider adding these to your resume:
            - Experience with: {}
            - Skills related to: {}
            """.format(
                ", ".join(keyword_comparison['missing'][:3]),
                ", ".join(keyword_comparison['missing'][3:6])
            ))
        else:
            st.success("All important keywords are covered in your resume.")

if __name__ == "__main__":
    main() 