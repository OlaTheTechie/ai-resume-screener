# AI Resume Screener

An AI-powered resume screening application built with Streamlit that helps both job candidates and hiring managers evaluate resume-job description matches.


![Project Picture](assets/ai-resume-screener.png "Optional title")

## Features

- Semantic similarity scoring using sentence transformers
- Keyword matching and analysis
- Improvement suggestions for candidates
- Candidate ranking for hiring managers
- CSV export functionality
- Support for PDF, DOCX, and TXT files

## Installation

1. Clone the repository:
```bash
git clone https://github.com/OlaTheTechie/ai-resume-screener.git
cd ai-resume-screener
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download the spaCy model:
```bash
python -m spacy download en_core_web_sm
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Choose your role:
   - **Candidate Mode**: Upload your resume and a job description to get feedback
   - **Manager Mode**: Upload multiple resumes and a job description to rank candidates


## Dependencies

- streamlit==1.32.0
- sentence-transformers==2.5.1
- PyPDF2==3.0.1
- spacy==3.7.4
- pandas==2.2.1
- python-docx==1.1.0
- nltk==3.8.1

## Contributing

Feel free to submit issues and enhancement requests! 
