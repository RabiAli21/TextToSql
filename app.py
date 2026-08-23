from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sqlite3
import os 
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_schema(db):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cur.fetchall()

    schema = ""

    for table in tables:
        table_name = table[0]

        cur.execute(f"PRAGMA table_info([{table_name}])")
        columns = cur.fetchall()

        schema += f"Table: {table_name}\n"
        schema += "Columns: " + ", ".join(column[1] for column in columns)
        schema += "\n\n"

    con.close()

    return schema

def get_response(question, prompt):

    model = genai.GenerativeModel("gemini-3.6-flash")
    schema = get_schema("revanstack.db")
    final_prompt = prompt[0].format(schema=schema)
    response = model.generate_content([final_prompt, question])
    return response.text.strip()


def read_sql(query, db):

    query = query.replace("```sql", "").replace("```", "").strip()

    if query.lower().startswith("cannot"):
        return []

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(query)
    rows = cur.fetchall()

    con.close()

    return rows



prompt = ["""
You are an expert SQL database manager.

Convert the user's question into a valid SQLite SQL query.

Rules:
- Use only the tables and columns in the schema.
- Do not invent table or column names.
- Return only the SQL query.
- Do not return explanations or markdown.

Schema:
{schema}
"""]

# streamlit App

st.set_page_config(page_title="SQL Expert", page_icon="🔍")

st.header("🤖 AI SQL Expert")

question = st.text_input("Input : ",key = "input")

submit = st.button("Ask")

if submit:
    response = get_response(question,prompt)
    print(response)
    data = read_sql(response,"revanstack.db")
    st.subheader("The Answer is : ")
    for row in data:
        print(row)
        st.subheader(row)
