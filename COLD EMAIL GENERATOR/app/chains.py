import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv('Groq_API_KEY'),
            model_name='meta-llama/llama-4-scout-17b-16e-instruct'
        )

    def extract_jobs(self, url):
        loader = WebBaseLoader(url)
        page_data = loader.load().pop().page_content

        prompt = PromptTemplate.from_template('''
        You are a job description extractor. Extract the following information from the job description:
        1. Job Title
        2. Company Name
        3. Location
        4. Job Description
        5. Required Skills
        6. Preferred Skills
        7. Responsibilities
        8. Qualifications
        9. Salary Range
        10. Benefits
        Extract the information from the following job description:
        {job_description}
        ''')

        chain = prompt | self.llm
        res = chain.invoke({'job_description': page_data})
        return res.content

    def write_email(self, job_description, portfolio_links):
        prompt = PromptTemplate.from_template('''
        You are Mohan, a business development executive at AtliQ. AtliQ is an AI & Software Consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools.

        Your job is to write a cold email to the client regarding the job mentioned below:

        Job Description: {job_description}

        Here are some relevant portfolio links based on the job requirements:
        {portfolio_links}

        Write a professional cold email that:
        1. Introduces AtliQ and its services
        2. Highlights how AtliQ can help with their specific needs
        3. Mentions relevant portfolio projects
        4. Requests a meeting or call

        Keep it concise and professional.
        ''')

        chain = prompt | self.llm
        res = chain.invoke({
            'job_description': job_description,
            'portfolio_links': portfolio_links
        })
        return res.content