import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/DFX-Software-QA-Test-Dev-Engineer_JR1998610?locationHierarchy1=2fcb99c455831013ea52b82135ba3266")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            portfolio.load_portfolio()
            job_info = llm.extract_jobs(url_input)

            # Extract skills from job description to query portfolio
            skills = [job_info]  # Use the job description to find relevant skills
            portfolio_links = portfolio.query_links(skills)

            email = llm.write_email(job_info, portfolio_links)
            st.markdown(email)
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)