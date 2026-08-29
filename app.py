from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import streamlit as st
import sqlite3
import os 
import google.generativeai as genai

if "history" not in st.session_state:
    st.session_state.history = []

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
    query = response.text.strip()

    query = query.replace("```sql", "")
    query = query.replace("```", "")

    return query.strip()


def read_sql(query, db):

    query = query.replace("```sql", "").replace("```", "").strip()

    if query.lower().startswith("cannot"):
        return None, "The question cannot be answered using the available data."

    try:
        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute(query)

        rows = cur.fetchall()

        columns = [description[0] for description in cur.description]

        con.close()

        df = pd.DataFrame(rows, columns=columns)

        return df, None

    except Exception as e:

        con.close()

        return None, str(e)



def fix_sql(query, error, question, schema):

    model = genai.GenerativeModel("gemini-3.6-flash")

    prompt = f"""
You are an expert SQLite SQL debugger.

User question:
{question}

Database schema:
{schema}

Generated SQL:
{query}

SQLite error:
{error}

Fix the SQL query so it correctly answers the user's question.

Rules:
- Use only tables and columns from the schema.
- Return only the corrected SQL query.
- Do not include markdown or explanations.
"""

    response = model.generate_content(prompt)

    fixed_query = response.text.strip()

    fixed_query = fixed_query.replace("```sql", "")
    fixed_query = fixed_query.replace("```", "")

    return fixed_query.strip()



def show_chart(df):

    if df is None or df.empty:
        return

    numeric_columns = df.select_dtypes(include="number").columns
    non_numeric_columns = df.select_dtypes(exclude="number").columns

    # Two numeric columns → Scatter chart
    if len(numeric_columns) >= 2:

        st.subheader("📊 Visualization")

        chart_data = df[[numeric_columns[0], numeric_columns[1]]].copy()

        st.scatter_chart(
            chart_data,
            x=numeric_columns[0],
            y=numeric_columns[1]
        )

        return

    # One numeric + one categorical/date column
    if len(numeric_columns) >= 1 and len(non_numeric_columns) >= 1:

        x_column = non_numeric_columns[0]
        y_column = numeric_columns[0]

        chart_data = df[[x_column, y_column]].copy()

        # Check whether the first column looks like a date
        date_column = pd.to_datetime(
            chart_data[x_column],
            errors="coerce"
        )

        if date_column.notna().sum() == len(chart_data):

            chart_data[x_column] = date_column
            chart_data = chart_data.sort_values(x_column)
            chart_data = chart_data.set_index(x_column)

            st.subheader("📈 Visualization")

            st.line_chart(chart_data[y_column])

        else:

            chart_data = chart_data.set_index(x_column)

            st.subheader("📊 Visualization")

            st.bar_chart(chart_data[y_column])


def explain_result(question, query, df):

    model = genai.GenerativeModel("gemini-3.6-flash")

    result = df.to_string(index=False)

    prompt = f"""
You are a data analyst.

Explain the SQL query result to the user in simple, clear English.

User question:
{question}

SQL query:
{query}

Query result:
{result}

Rules:
- Explain what the result means.
- Mention the most important findings.
- Use actual values from the result.
- Keep the explanation concise.
- Do not explain the SQL syntax.
- Do not invent information that is not present in the result.
"""

    response = model.generate_content(prompt)

    return response.text.strip()



prompt = ["""
You are an expert SQL database manager.

Convert the user's question into a valid SQLite SQL query.

Rules:
- Use only tables and columns from the schema.
- Do not invent table or column names.
- Return only the SQL query.
- Do not return explanations or markdown.
- Format the SQL query on multiple lines so it is easy to read.
- Put SELECT, FROM, JOIN, WHERE, GROUP BY, ORDER BY and LIMIT on separate lines when applicable.
- Use proper indentation for columns and conditions.

Database Schema:
{schema}
"""]

# streamlit App

st.set_page_config(page_title="SQL Expert", page_icon="🔍")
with st.sidebar:

    st.header("🕘 Query History")

    if st.session_state.history:

        for i, item in enumerate(
            reversed(st.session_state.history),
            1
        ):
            st.write(f"{i}. {item}")

    else:

        st.write("No queries yet.")

st.title("🤖 AI Analytics Assistant")
st.caption("Ask questions about your data in natural language")

question = st.text_input("Input : ",key = "input")

submit = st.button("Ask")

if submit:

    response = get_response(question, prompt)

    # Save question to history
    st.session_state.history.append(question)

    st.subheader("💻 Generated SQL")
    st.code(response, language="sql")

    data, error = read_sql(response, "revanstack.db")

    if error:

        st.warning("SQL query failed. AI is correcting the query...")

        schema = get_schema("revanstack.db")

        fixed_query = fix_sql(
            response,
            error,
            question,
            schema
        )

        st.subheader("🔧 Corrected SQL")
        st.code(fixed_query, language="sql")

        data, error = read_sql(
            fixed_query,
            "revanstack.db"
        )

        if error:

            st.error(f"SQL Error: {error}")

        else:

            st.success("Query automatically corrected!")

            st.subheader("📋 Query Result")
            st.dataframe(
                data,
                use_container_width=True
            )

            show_chart(data)

            st.subheader("📝 AI Analysis")

            explanation = explain_result(
                question,
                fixed_query,
                data
            )

            st.write(explanation)

    else:

        st.subheader("📋 Query Result")
        st.dataframe(
            data,
            use_container_width=True
        )

        show_chart(data)

        st.subheader("📝 AI Analysis")

        explanation = explain_result(
            question,
            response,
            data
        )

        st.write(explanation)
