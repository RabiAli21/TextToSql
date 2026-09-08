from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import streamlit as st
import sqlite3
import os 
from openai import OpenAI
import matplotlib.pyplot as plt 
import seaborn as sns
import mysql.connector

if "history" not in st.session_state:
    st.session_state.history = []

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

GROQ_MODEL = "openai/gpt-oss-120b"

def ask_ai(prompt):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env file")
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def connect_mysql(host, port, user, password, database):
    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )


def get_schema(db_type, db, mysql_config=None):

    schema = ""

    if db_type == "SQLite":

        con = sqlite3.connect(db)
        cur = con.cursor()

        cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
        """)

        tables = [row[0] for row in cur.fetchall()]

        for table_name in tables:
            cur.execute(f'PRAGMA table_info("{table_name}")')
            columns = cur.fetchall()
            schema += f"Table: {table_name}\n"
            schema += "Columns: " + ", ".join(column[1] for column in columns)
            schema += "\n\n"

        con.close()

    else:

        con = connect_mysql(**mysql_config)
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        tables = [row[0] for row in cur.fetchall()]

        for table_name in tables:
            cur.execute(f'DESCRIBE `{table_name}`')
            columns = cur.fetchall()
            schema += f"Table: {table_name}\n"
            schema += "Columns: " + ", ".join(column[0] for column in columns)
            schema += "\n\n"

        cur.close()
        con.close()

    return schema


def get_database_info(db_type, db, mysql_config=None):

    database_info = {}

    if db_type == "SQLite":
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
        """)
        tables = [row[0] for row in cur.fetchall()]

        for table in tables:
            cur.execute(f'PRAGMA table_info("{table}")')
            columns = cur.fetchall()
            cur.execute(f'SELECT COUNT(*) FROM "{table}"')
            row_count = cur.fetchone()[0]
            database_info[table] = {
                "rows": row_count,
                "columns": [
                    {
                        "name": column[1],
                        "type": column[2],
                        "not_null": column[3],
                        "primary_key": column[5]
                    }
                    for column in columns
                ]
            }
        con.close()

    else:
        con = connect_mysql(**mysql_config)
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        tables = [row[0] for row in cur.fetchall()]

        for table in tables:
            cur.execute(f'DESCRIBE `{table}`')
            columns = cur.fetchall()
            cur.execute(f'SELECT COUNT(*) FROM `{table}`')
            row_count = cur.fetchone()[0]
            database_info[table] = {
                "rows": row_count,
                "columns": [
                    {
                        "name": column[0],
                        "type": column[1],
                        "not_null": 1 if column[2] == "NO" else 0,
                        "primary_key": 1 if column[3] == "PRI" else 0
                    }
                    for column in columns
                ]
            }
        cur.close()
        con.close()

    return database_info


def get_sample_data(table, db_type, db, mysql_config=None, limit=5):

    if db_type == "SQLite":
        con = sqlite3.connect(db)
        df = pd.read_sql_query(
            f'SELECT * FROM "{table}" LIMIT {limit}',
            con
        )
        con.close()
    else:
        con = connect_mysql(**mysql_config)
        df = pd.read_sql_query(
            f'SELECT * FROM `{table}` LIMIT {limit}',
            con
        )
        con.close()

    return df


def explain_database(db_type, db, mysql_config=None):

    database_info = get_database_info(db_type, db, mysql_config)
    schema_text = ""

    for table, info in database_info.items():
        schema_text += f"\nTable: {table}\n"
        schema_text += f"Rows: {info['rows']}\n"
        schema_text += "Columns:\n"
        for column in info["columns"]:
            schema_text += f"- {column['name']} ({column['type']})\n"

    prompt = f"""
You are a senior data analyst.

Analyze the following database structure and explain it
to a non-technical user.

DATABASE TYPE:
{db_type}

DATABASE INFORMATION:
{schema_text}

Explain:
1. What this database appears to contain.
2. What each table represents.
3. Important columns in each table.
4. Possible relationships between tables.
5. What kind of business analysis can be performed.
6. Useful questions a user could ask.
7. Any obvious data-quality considerations based only on the provided information.

Rules:
- Use only the provided information.
- Do not invent facts.
- Keep the explanation clear and concise.
- Use headings and bullet points.
"""

    return ask_ai(prompt)


def get_response(question, prompt, db_type, db, mysql_config=None):

    schema = get_schema(db_type, db, mysql_config)
    final_prompt = prompt[0].format(
        schema=schema,
        database_type=db_type
    )
    query = ask_ai(final_prompt + "\n\nUSER QUESTION:\n" + question)
    query = query.replace("```sql", "").replace("```", "")
    return query.strip()


def read_mysql(query, host, port, user, password, database):

    connection = None

    try:
        connection = connect_mysql(
            host, port, user, password, database
        )
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        cursor.close()
        connection.close()
        return df, None

    except Exception as e:
        if connection:
            connection.close()
        return None, str(e)


def execute_query(query, db_type, db, mysql_config=None):
    if db_type == "SQLite":
        return read_sql(query, db)
    return read_mysql(query, **mysql_config)


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



def fix_sql(query, error, question, schema, db_type):

    prompt = f"""
You are an expert SQL debugger.

Database type:
{db_type}

User question:
{question}

Database schema:
{schema}

Generated SQL:
{query}

Database error:
{error}

Fix the SQL query so it correctly answers the user's question.

Rules:
- Use only tables and columns from the schema.
- Use SQL syntax appropriate for {db_type}.
- Return only the corrected SQL query.
- Do not include markdown or explanations.
"""
    fixed_query = ask_ai(prompt)
    fixed_query = fixed_query.replace("```sql", "").replace("```", "")
    return fixed_query.strip()


def show_chart(question, query, df):

    if df is None or df.empty:
        return

    st.subheader("📊 AI Visualization")

    with st.spinner(
        "AI is selecting the best visualization..."
    ):

        recommendation = get_chart_recommendation(
            question,
            query,
            df
        )

    validated = validate_chart_recommendation(
        recommendation,
        question,
        df
    )

    if validated is None:

        st.info(
            "No suitable visualization could be determined."
        )

        return

    chart_type = validated.get(
        "chart_type",
        "none"
    )

    if chart_type == "none":

        st.info(
            "This result is better represented as a table."
        )

        return

    st.caption(
        f"AI selected: {chart_type.title()} chart"
    )

    create_visualization(
        recommendation,
        df
    )


def get_chart_recommendation(question, query, df):


    columns = list(df.columns)

    sample_data = df.head(20).to_string(index=False)

    prompt = f"""
You are an expert data visualization analyst.

Your job is to select the BEST chart for the SQL RESULT.

USER QUESTION:
{question}

SQL QUERY:
{query}

RESULT COLUMNS:
{columns}

RESULT DATA:
{sample_data}

IMPORTANT:
The user's question is the most important instruction.

If the user asks:
- "by industry" → industry must be the X-axis.
- "by account" → account/account_name must be the X-axis.
- "by country" → country must be the X-axis.
- "by month" → month/date must be the X-axis.
- "by year" → year must be the X-axis.
- "over time" → use a date/time column.
- "relationship between X and Y" → use scatter chart.

Do NOT select a date/month column unless the user asks for
time, month, year, date, trend, or over time.

Choose from:

bar
line
scatter
histogram
pie
none

Return ONLY:

chart_type: bar
x_column: exact_column_name
y_column: exact_column_name
title: Chart Title

Rules:
- x_column MUST exist in the result columns.
- y_column MUST exist in the result columns.
- Use bar for category comparisons.
- Use line ONLY for time-based trends.
- Use scatter ONLY for two numerical variables.
- Use histogram for one numerical distribution.
- Use pie only for small part-to-whole comparisons.
- Use none if no meaningful visualization is possible.
- Never invent columns.
- Never use columns that are not in the result.
- Follow the user's requested grouping exactly.
"""

    return ask_ai(prompt)


def validate_chart_recommendation(recommendation, question, df):

    lines = recommendation.splitlines()

    result = {}

    for line in lines:

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        result[key.strip().lower()] = value.strip()

    chart_type = result.get("chart_type", "none").lower()
    x_column = result.get("x_column", "")
    y_column = result.get("y_column", "")

    valid_chart_types = [
        "bar",
        "line",
        "scatter",
        "histogram",
        "pie",
        "none"
    ]

    if chart_type not in valid_chart_types:
        return None

    if chart_type == "none":
        return result

    if chart_type != "histogram":

        if x_column not in df.columns:
            return None

    if y_column and y_column not in df.columns:
        return None

    # Prevent line charts unless the question asks for time
    time_words = [
        "month",
        "monthly",
        "year",
        "yearly",
        "date",
        "daily",
        "weekly",
        "trend",
        "over time",
        "time"
    ]

    question_lower = question.lower()

    if (
        chart_type == "line"
        and not any(word in question_lower for word in time_words)
    ):
        return None

    return result


def create_visualization(recommendation, df):

    lines = recommendation.splitlines()

    chart_type = ""
    x_column = ""
    y_column = ""
    title = "AI Generated Visualization"

    for line in lines:

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip().lower()
        value = value.strip()

        if key == "chart_type":
            chart_type = value.lower()

        elif key == "x_column":
            x_column = value

        elif key == "y_column":
            y_column = value

        elif key == "title":
            title = value

    if chart_type == "none":
        return

    if (
        x_column not in df.columns
        and chart_type not in ["histogram"]
    ):
        return

    if (
        y_column not in df.columns
        and chart_type not in ["histogram"]
    ):
        return

    fig = None

    if chart_type == "bar":

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        sns.barplot(
            data=df,
            x=x_column,
            y=y_column,
            ax=ax
        )

        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        ax.tick_params(
            axis="x",
            rotation=45
        )

    elif chart_type == "line":

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        sns.lineplot(
            data=df,
            x=x_column,
            y=y_column,
            marker="o",
            ax=ax
        )

        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

        ax.tick_params(
            axis="x",
            rotation=45
        )

    elif chart_type == "scatter":

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        sns.scatterplot(
            data=df,
            x=x_column,
            y=y_column,
            ax=ax
        )

        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)

    elif chart_type == "histogram":

        if y_column in df.columns:

            fig, ax = plt.subplots(
                figsize=(10, 6)
            )

            sns.histplot(
                data=df,
                x=y_column,
                kde=True,
                ax=ax
            )

            ax.set_title(title)
            ax.set_xlabel(y_column)

    elif chart_type == "pie":

        fig, ax = plt.subplots(
            figsize=(8, 8)
        )

        df.set_index(x_column)[
            y_column
        ].plot.pie(
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_title(title)
        ax.set_ylabel("")

    if fig is not None:

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)


def explain_result(question, query, df):


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

    return ask_ai(prompt)



prompt = ["""
You are an expert SQL database manager.

Convert the user's question into a valid SQL query for the selected database.

Database type:
{database_type}

Rules:
- Use only tables and columns from the schema.
- Do not invent table or column names.
- Use SQL syntax appropriate for the selected database.
- Return only the SQL query.
- Do not return explanations or markdown.
- Format the SQL query on multiple lines so it is easy to read.
- Put SELECT, FROM, JOIN, WHERE, GROUP BY, ORDER BY and LIMIT on separate lines when applicable.
- Use proper indentation for columns and conditions.

Database Schema:
{schema}
"""]

# ==============================
# STREAMLIT APP
# ==============================

st.set_page_config(
    page_title="AI Analytics Assistant",
    page_icon="🤖"
)


# ==============================
# DATABASE DEFAULTS
# ==============================

DB = "revanstack.db"

database_type = "SQLite"
mysql_host = ""
mysql_port = 3306
mysql_user = ""
mysql_password = ""
mysql_database = ""


# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.title("🤖 AI Analytics")

    page = st.radio(
        "Navigation",
        [
            "💬 SQL Assistant",
            "🗂️ Database Schema"
        ]
    )

    st.divider()

    st.subheader("🗄️ Database")

    database_type = st.radio(
        "Select database",
        ["SQLite", "MySQL"],
        key="database_type"
    )

    if database_type == "MySQL":

        st.subheader("🔐 MySQL Connection")

        mysql_host = st.text_input(
            "Host",
            value="localhost"
        )

        mysql_port = st.number_input(
            "Port",
            value=3306,
            step=1
        )

        mysql_user = st.text_input(
            "Username"
        )

        mysql_password = st.text_input(
            "Password",
            type="password"
        )

        mysql_database = st.text_input(
            "Database"
        )

        if st.button("🔌 Test MySQL Connection"):

            try:
                connection = connect_mysql(
                    mysql_host,
                    mysql_port,
                    mysql_user,
                    mysql_password,
                    mysql_database
                )

                if connection.is_connected():
                    st.success("✅ MySQL connection successful!")

                connection.close()

            except Exception as e:
                st.error(f"❌ MySQL connection failed: {e}")

    st.divider()

    st.header("🕘 Query History")

    if st.session_state.history:

        for i, item in enumerate(
            reversed(st.session_state.history),
            1
        ):
            st.write(f"{i}. {item}")

    else:

        st.write("No queries yet.")


# ==============================
# MYSQL CONFIGURATION
# ==============================

mysql_config = {
    "host": mysql_host,
    "port": mysql_port,
    "user": mysql_user,
    "password": mysql_password,
    "database": mysql_database
}


# ==============================
# SQL ASSISTANT PAGE
# ==============================

if page == "💬 SQL Assistant":

    st.title("🤖 AI Analytics Assistant")

    st.caption(
        "Ask questions about your data in natural language"
    )

    question = st.text_input(
        "Ask your question:",
        key="input"
    )

    submit = st.button("🔍 Ask")


    # ==============================
    # SQL QUERY EXECUTION
    # ==============================

    if submit:

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            response = get_response(
                question,
                prompt,
                database_type,
                DB,
                mysql_config
            )

            # Save question to history
            st.session_state.history.append(
                question
            )

            st.subheader("💻 Generated SQL")

            st.code(
                response,
                language="sql"
            )

            data, error = execute_query(
                response,
                database_type,
                DB,
                mysql_config
            )


            # ==============================
            # SQL ERROR CORRECTION
            # ==============================

            if error:

                st.warning(
                    "SQL query failed. "
                    "AI is correcting the query..."
                )

                schema = get_schema(
                    database_type,
                    DB,
                    mysql_config
                )

                fixed_query = fix_sql(
                    response,
                    error,
                    question,
                    schema,
                    database_type
                )

                st.subheader(
                    "🔧 Corrected SQL"
                )

                st.code(
                    fixed_query,
                    language="sql"
                )

                data, error = execute_query(
                    fixed_query,
                    database_type,
                    DB,
                    mysql_config
                )


                if error:

                    st.error(
                        f"SQL Error: {error}"
                    )

                else:

                    st.success(
                        "Query automatically corrected!"
                    )

                    st.subheader(
                        "📋 Query Result"
                    )

                    st.dataframe(
                        data,
                        use_container_width=True
                    )

                    show_chart(
                        question,
                        fixed_query,
                        data
                    )

                    st.subheader(
                        "📝 AI Analysis"
                    )

                    explanation = explain_result(
                        question,
                        fixed_query,
                        data
                    )

                    st.write(
                        explanation
                    )


            # ==============================
            # SUCCESSFUL QUERY
            # ==============================

            else:

                st.subheader(
                    "📋 Query Result"
                )

                st.dataframe(
                    data,
                    use_container_width=True
                )

                show_chart(
                    question,
                    response,
                    data
                )

                st.subheader(
                    "📝 AI Analysis"
                )

                explanation = explain_result(
                    question,
                    response,
                    data
                )

                st.write(
                    explanation
                )


# ==============================
# DATABASE SCHEMA PAGE
# ==============================

if page == "🗂️ Database Schema":

    st.title(
        "🗄️ Database Schema"
    )

    st.caption(
        "Explore tables, columns, rows and sample data"
    )

    database_info = get_database_info(
        database_type,
        DB,
        mysql_config
    )


    # ==============================
    # SCHEMA TABS
    # ==============================

    tab1, tab2, tab3 = st.tabs([
        "📊 Overview",
        "📋 Tables",
        "🤖 AI Data Guide"
    ])


    # ==============================
    # OVERVIEW
    # ==============================

    with tab1:

        total_tables = len(
            database_info
        )

        total_rows = sum(
            info["rows"]
            for info in database_info.values()
        )

        total_columns = sum(
            len(info["columns"])
            for info in database_info.values()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Tables",
            total_tables
        )

        col2.metric(
            "Total Rows",
            f"{total_rows:,}"
        )

        col3.metric(
            "Total Columns",
            total_columns
        )


    # ==============================
    # TABLES
    # ==============================

    with tab2:

        table_names = list(
            database_info.keys()
        )

        table_tabs = st.tabs(
            table_names
        )

        for table_tab, table_name in zip(
            table_tabs,
            table_names
        ):

            with table_tab:

                info = database_info[
                    table_name
                ]

                st.subheader(
                    f"📋 {table_name}"
                )

                col1, col2 = st.columns(2)

                col1.metric(
                    "Rows",
                    f"{info['rows']:,}"
                )

                col2.metric(
                    "Columns",
                    len(info["columns"])
                )

                st.markdown(
                    "### 🧱 Columns"
                )

                column_data = []

                for column in info["columns"]:

                    column_data.append({

                        "Column": column["name"],

                        "Data Type": column["type"],

                        "Not Null":
                            "Yes"
                            if column["not_null"]
                            else "No",

                        "Primary Key":
                            "Yes"
                            if column["primary_key"]
                            else "No"
                    })

                column_df = pd.DataFrame(
                    column_data
                )

                st.dataframe(
                    column_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown(
                    "### 👀 Sample Data"
                )

                sample_df = get_sample_data(
                    table_name,
                    database_type,
                    DB,
                    mysql_config
                )

                st.dataframe(
                    sample_df,
                    use_container_width=True,
                    hide_index=True
                )


    # ==============================
    # AI DATA GUIDE
    # ==============================

    with tab3:

        st.subheader(
            "🤖 AI Data Guide"
        )

        st.write(
            "Let Gemini analyze your database "
            "structure and explain what the "
            "data contains."
        )

        if st.button(
            "🔍 Analyze Database"
        ):

            with st.spinner(
                "AI is analyzing your database..."
            ):

                explanation = explain_database(
                    database_type,
                    DB,
                    mysql_config
                )

            st.markdown(
                explanation
            )

