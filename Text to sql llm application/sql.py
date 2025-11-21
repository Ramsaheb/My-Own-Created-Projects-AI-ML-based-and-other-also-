from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
import streamlit as st
import requests
import json
from pymongo import MongoClient
import pandas as pd

# MongoDB connection
def get_mongo_client():
    try:
        # Update with your MongoDB connection string
        MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(MONGO_URI)
        return client
    except Exception as e:
        st.error(f"MongoDB connection error: {str(e)}")
        return None

def get_llama_response(question, prompt):
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2',
                'prompt': prompt[0] + question,
                'stream': False,
                'options': {
                    'temperature': 0.1,
                }
            },
            timeout=120
        )
        return response.json()['response']
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        raise e

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

def query_mongodb(question, prompt):
    """Generate MongoDB query and execute it"""
    try:
        # Get MongoDB query from LLM
        mongo_query = get_llama_response(question, prompt)
        mongo_query = mongo_query.strip().replace('```python', '').replace('```json', '').replace('```', '').strip()
        
        # Connect to MongoDB
        client = get_mongo_client()
        if not client:
            return None, None
        
        db = client['text_to_sql']
        collection = db['students']
        
        # Parse the query string to dict
        try:
            query_dict = eval(mongo_query) if mongo_query.startswith('{') else {}
            
            # Fix common issues - if all values are empty strings, use empty dict
            if all(v == "" or v == {} for v in query_dict.values()):
                query_dict = {}
                mongo_query = "{}"  # Update display
                
        except:
            query_dict = {}
            mongo_query = "{}"
        
        # Execute query
        results = list(collection.find(query_dict))
        
        client.close()
        return results, mongo_query
    except Exception as e:
        st.error(f"MongoDB Error: {str(e)}")
        return None, None

sql_prompt = [
    '''
You are an expert SQL developer. Given a question in plain English, generate ONLY the SQL query without any additional text, explanations, or markdown formatting.

Database Schema:
STUDENT(NAME VARCHAR(50), AGE INT, CLASS VARCHAR(10), SECTION VARCHAR(5), MARKS INT, SUBJECT VARCHAR(30), ATTENDANCE FLOAT, CITY VARCHAR(30))

Important Rules:
1. Generate only the SQL query, nothing else
2. Do not include SQL code block markers, backticks, or explanations
3. Use proper SQL syntax for SQLite
4. Column names are case-sensitive
5. For string comparisons, use single quotes
6. Return SELECT queries that can be directly executed
7. When asked about "same class/age/marks", show ALL records ordered by that column
8. Use ORDER BY to group similar values together

Examples:

Question: "List all students in class 8th."
SQL: SELECT * FROM STUDENT WHERE CLASS = '8th';

Question: "How many students are in section A?"
SQL: SELECT COUNT(*) FROM STUDENT WHERE SECTION = 'A';

Question: "Show names of students who scored more than 90 marks."
SQL: SELECT NAME FROM STUDENT WHERE MARKS > 90;

Now generate the SQL query for the following question:
'''
]

mongo_prompt = [
    '''
You are an expert MongoDB developer. Given a question in plain English, generate ONLY the MongoDB query as a Python dictionary without any additional text or explanations.

Database Schema:
Collection: students
Fields: {name: string, age: int, class: string, section: string, marks: int, subject: string, attendance: float, city: string}

Important Rules:
1. Generate only the MongoDB query dictionary, nothing else
2. Do not include code block markers, backticks, or explanations
3. Use proper MongoDB query syntax
4. Field names are lowercase
5. Return valid Python dictionary that can be used with collection.find()
6. For "all students" or "show details", return empty dictionary: {}
7. Use MongoDB operators: $gt, $lt, $gte, $lte, $eq, $in, etc.

Examples:

Question: "Show all students."
MongoDB: {}

Question: "Display details of all students."
MongoDB: {}

Question: "List all students in class 8th."
MongoDB: {"class": "8th"}

Question: "Show students who scored more than 90 marks."
MongoDB: {"marks": {"$gt": 90}}

Question: "Find students from New York with attendance above 90%."
MongoDB: {"city": "New York", "attendance": {"$gt": 90}}

Question: "Students in section A."
MongoDB: {"section": "A"}

Question: "Find students aged 14."
MongoDB: {"age": 14}

Now generate the MongoDB query for the following question:
'''
]

st.set_page_config(page_title="SQL/MongoDB Query Generator", layout="wide")
st.header("🤖 SQL/MongoDB Query Generator with Llama 3.2")

# Database selection
db_type = st.sidebar.radio("Select Database Type:", ["SQLite", "MongoDB"])

# Add sidebar with info
with st.sidebar:
    st.header("📊 Database Schema")
    if db_type == "SQLite":
        st.code("""
STUDENT(
    NAME VARCHAR(50),
    AGE INT,
    CLASS VARCHAR(10),
    SECTION VARCHAR(5),
    MARKS INT,
    SUBJECT VARCHAR(30),
    ATTENDANCE FLOAT,
    CITY VARCHAR(30)
)
        """, language="sql")
    else:
        st.code("""
Collection: students
{
    name: string,
    age: int,
    class: string,
    section: string,
    marks: int,
    subject: string,
    attendance: float,
    city: string
}
        """, language="json")
    
    st.info(f"💡 Using Llama 3.2 running locally via Ollama")

# Example questions
with st.expander("💡 Example Questions"):
    examples = [
        "List all students in class 8th",
        "How many students are in section A?",
        "Show names of students who scored more than 90 marks",
        "Find students from New York with attendance above 90%",
        "What is the average attendance of 9th class students?",
        "Display students grouped by their class"
    ]
    for ex in examples:
        st.text(f"• {ex}")

question = st.text_input("Enter your question about the STUDENT database:", 
                         placeholder="e.g., List all students in class 8th")

submit = st.button("Generate Query", type="primary")

if submit:
    if question:
        with st.spinner(f"Generating {db_type} query with Llama..."):
            try:
                if db_type == "SQLite":
                    # SQL Query
                    sql = get_llama_response(question, sql_prompt)
                    sql = sql.strip().replace('```sql', '').replace('```', '').strip()
                    
                    st.subheader("✅ Generated SQL Query:")
                    st.code(sql, language="sql")
                    
                    st.subheader("📊 Query Results:")
                    rows = read_sql_query(sql, "Student.db")
                    
                    if rows:
                        st.dataframe(rows, use_container_width=True)
                        st.success(f"Found {len(rows)} record(s)")
                    else:
                        st.info("No results found.")
                
                else:
                    # MongoDB Query
                    results, mongo_query = query_mongodb(question, mongo_prompt)
                    
                    st.subheader("✅ Generated MongoDB Query:")
                    st.code(mongo_query, language="python")
                    
                    st.subheader("📊 Query Results:")
                    
                    if results:
                        df = pd.DataFrame(results)
                        if '_id' in df.columns:
                            df = df.drop('_id', axis=1)
                        st.dataframe(df, use_container_width=True)
                        st.success(f"Found {len(results)} record(s)")
                    else:
                        st.info("No results found.")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a question.")