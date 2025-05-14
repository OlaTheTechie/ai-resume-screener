import streamlit as st
import sys
import os
import pandas as pd
from pathlib import Path
from typing import List, Dict
import tempfile

# adding parent directory to path (because I'm lazy)
sys.path.append(str(Path(__file__).parent.parent))

from utils.text_extraction import extract_text_from_file, preprocess_text
from utils.similarity import calculate_similarity, extract_keywords, compare_keywords

def process_resumes(resume_files: List, job_desc: str) -> pd.DataFrame:
    # processing all the resumes
    results = []
    
    for resume_file in resume_files:
        # getting text from resume
        resume_text = extract_text_from_file(resume_file)
        resume_text = preprocess_text(resume_text)
        
        # calculating match
        similarity_score = calculate_similarity(resume_text, job_desc)
        
        # keyword stuff
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_desc)
        keyword_comparison = compare_keywords(resume_keywords, job_keywords)
        
        # saving results
        results.append({
            'Resume': resume_file.name,
            'Match Score': similarity_score,
            'Keywords Hit': len(keyword_comparison['matched']),
            'Keywords Missed': len(keyword_comparison['missing']),
            'Keywords Hit List': ', '.join(keyword_comparison['matched']),
            'Keywords Missed List': ', '.join(keyword_comparison['missing'])
        })
    
    # making it pretty with pandas
    df = pd.DataFrame(results)
    df = df.sort_values('Match Score', ascending=False)
    return df

def main():
    st.title("Manager Mode")
    st.markdown("""
    Upload multiple resumes and a job description to:
    - View ranked candidates
    - Compare keyword matches
    - Export results as CSV
    """)

    # file upload section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resumes")
        resume_files = st.file_uploader(
            "Upload multiple resumes (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True
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

    if resume_files and (job_desc_file or job_desc_text):
        # processing job description
        if job_desc_file:
            job_desc = extract_text_from_file(job_desc_file)
        else:
            job_desc = job_desc_text
        job_desc = preprocess_text(job_desc)
        
        # processing all resumes
        with st.spinner("Processing resumes..."):
            results_df = process_resumes(resume_files, job_desc)
        
        # showing results
        st.markdown("---")
        st.subheader("Analysis Results")
        
        # top matches
        st.markdown("### Top Candidates")
        top_candidates = results_df[['Resume', 'Match Score', 'Keywords Hit', 'Keywords Missed']]
        st.dataframe(top_candidates.style.format({'Match Score': '{:.1%}'}))
        
        # detailed view
        st.markdown("### Detailed Analysis")
        for _, row in results_df.iterrows():
            with st.expander(f"{row['Resume']} ({row['Match Score']:.1%})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Matched Keywords**")
                    st.write(row['Keywords Hit List'])
                with col2:
                    st.markdown("**Missing Keywords**")
                    st.write(row['Keywords Missed List'])
        
        # download button
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="Download Results",
            data=csv,
            file_name="resume_analysis.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 