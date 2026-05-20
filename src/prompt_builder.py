import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def build_prompt(question, schema):
    prompt = f""" You are an expert SQL assistant. Given a database schema and a user question, 
    generate a valid SQL query that answers the question.
    Return ONLY the SQL query, no explanation, no markdown, no backticks.
    Use proper JOIN syntax when querying multiple tables.
    Do not use comma-separated tables in the FROM clause.
    
    Schema: {schema}

    Question: {question}

    SQL:"""
    
    return prompt

def generate_sql(prompt):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


