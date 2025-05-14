import streamlit as st
import os

# making things pretty
st.set_page_config(
    page_title="Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# my attempt at CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("Resume Screener")
    st.markdown("""
    Welcome to the Resume Screener. This tool helps evaluate resume-job description matches.
    
    Features:
    - Semantic similarity scoring
    - Keyword matching
    - Improvement suggestions
    - Candidate ranking
    
    How to Use:
    1. Select your role (Candidate or Manager)
    2. Upload your documents
    3. Get analysis and feedback
    
    Select your role from the sidebar to begin.
    """)

    # sidebar stuff
    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    Select Your Role:
    - Candidate Mode: Upload resume and job description
    - Manager Mode: Upload multiple resumes and job description
    """)

if __name__ == "__main__":
    main() 