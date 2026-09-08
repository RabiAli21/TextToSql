🤖 AI Analytics Assistant — Natural Language to SQL

An AI-powered analytics assistant that lets users interact with SQLite and MySQL databases using natural language instead of manually writing SQL.

🚀 Project Overview

The application converts a user's natural-language question into SQL using an LLM through the Groq API, executes the query against the selected database, displays the result, corrects SQL errors when possible, generates AI insights, and recommends suitable visualizations.

Example

User:

What is the total MRR by industry?

The application:

Retrieves the database schema.

Sends the schema and question to the AI.

Generates SQL.

Executes the SQL.

Displays the result.

Attempts automatic SQL correction if execution fails.

Generates an AI explanation.

Selects and generates an appropriate chart.

✨ Features

🧠 Natural Language → SQL

🗄️ SQLite support

🐬 MySQL support

🔌 MySQL connection testing

🔍 Dynamic Schema Explorer

🤖 AI Database Guide

🛠️ Automatic SQL Error Correction

📋 Query Result Display

📝 AI Result Analysis

📊 AI-Powered Visualization

🕘 Query History

📈 Bar, Line, Scatter, Histogram and Pie charts

🏗️ System Architecture

                    User Question
                          ↓
                    Streamlit UI
                          ↓
                       Groq API
                          ↓
              Schema + User Question
                          ↓
                    SQL Generation
                          ↓
                 SQLite / MySQL
                          ↓
                   Query Result
                          ↓
             ┌────────────┼────────────┐
             ↓            ↓            ↓
        AI Analysis   AI Chart     Result Table
                       Selection
                          ↓
                   Matplotlib /
                     Seaborn

🧰 Technology Stack

Category

Technology

Language

Python

AI / LLM

Groq API

AI Model

openai/gpt-oss-120b

LLM Client

OpenAI Python SDK

Web Framework

Streamlit

Databases

SQLite, MySQL

Data Processing

Pandas

Visualization

Matplotlib, Seaborn

Environment Variables

python-dotenv

MySQL Connector

mysql-connector-python

Version Control

Git / GitHub

📁 Project Structure

TextToSql/
│
├── app1.py
├── app.py
├── sql.py
├── revanstack.db
├── .env
├── .gitignore
├── README.md
│
└── dataset/
    ├── ravenstack_accounts.csv
    ├── ravenstack_churn_events.csv
    ├── ravenstack_feature_usage.csv
    ├── ravenstack_subscriptions.csv
    └── ravenstack_support_tickets.csv

app1.py is the Groq-powered application.

🔑 Environment Variables

Create a .env file in the project directory:

GROQ_API_KEY=your_groq_api_key

Never commit your API key to GitHub.

Add .env to .gitignore:

.env

⚙️ Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd TextToSql

2. Create a virtual environment

python -m venv venv

Windows:

venv\Scripts\activate

3. Install dependencies

pip install streamlit pandas matplotlib seaborn python-dotenv mysql-connector-python openai

4. Add your Groq API key

Create .env:

GROQ_API_KEY=your_groq_api_key

5. Run the application

streamlit run app1.py

💬 Example Questions

Account Analysis

How many accounts are there?

Show the number of accounts by industry.

Which country has the most accounts?

Revenue Analysis

What is the total MRR?

What is the total MRR by industry?

Which industry generates the highest MRR?

Show MRR by month.

Customer Analysis

How many customers have churned?

Show the churn count by reason.

Which customer segment has the highest churn?

Support Analysis

How many support tickets are there?

Show support tickets by priority.

Which category has the most support tickets?

Feature Usage

Which features are used the most?

Show average feature usage by account.

🔄 Application Workflow

1. User enters a question
             ↓
2. Application retrieves database schema
             ↓
3. Question + schema sent to Groq
             ↓
4. AI generates SQL
             ↓
5. SQL displayed to the user
             ↓
6. Query executed
             ↓
7. If error → AI corrects SQL
             ↓
8. Result displayed as a DataFrame
             ↓
9. AI analyzes the result
             ↓
10. AI recommends a visualization
             ↓
11. Matplotlib/Seaborn generates chart

🧠 Prompt Engineering

The project uses schema-aware prompting.

The AI receives:

Database Type
       +
Database Schema
       +
User Question

The model is instructed to:

Use only existing tables.

Use only existing columns.

Follow the selected database dialect.

Return only SQL for SQL-generation tasks.

Avoid inventing database objects.

Format generated SQL clearly.

This helps reduce invalid table and column names.

🛠️ Automatic SQL Error Correction

When generated SQL fails:

Generated SQL
      ↓
Execute Query
      ↓
   Error?
      ↓
Schema + Question + SQL + Error
      ↓
      Groq
      ↓
Corrected SQL
      ↓
Execute Again

The corrected query is displayed to the user.

📊 AI-Powered Visualization

The AI receives the user's question, SQL query, result columns, and sample result data.

It recommends:

Bar chart

Line chart

Scatter plot

Histogram

Pie chart

No chart when visualization is not meaningful

The application validates the recommendation before generating the chart.

Example:

Question:
Total MRR by industry

AI Recommendation:
Bar Chart

X-axis → Industry
Y-axis → Total MRR

🔍 Schema Explorer

The Schema Explorer provides:

Table names

Row counts

Column counts

Column names

Data types

NULL / NOT NULL information

Primary-key information

Sample data

It works with both SQLite and MySQL.

🤖 AI Database Guide

The AI Database Guide analyzes the selected database structure and explains:

What the database appears to contain.

What each table represents.

Important columns.

Possible relationships.

Potential business analysis.

Useful questions.

Basic data-quality considerations.

📝 AI Result Analysis

After a query executes successfully, the application sends the result to the AI and generates a concise explanation based on the returned data.

The AI is instructed not to invent findings that are not present in the query result.

🕘 Query History

The sidebar stores questions asked during the current Streamlit session.

Example:

🕘 Query History

1. Total MRR by industry
2. Number of accounts by country
3. Average subscription value
4. Total support tickets

🔐 Security

API credentials are loaded from environment variables:

os.getenv("GROQ_API_KEY")

Do not hard-code API keys in source code.

Do not commit .env to GitHub.

📌 Current Capabilities

Feature

Status

Natural Language → SQL

✅

Groq Integration

✅

SQLite

✅

MySQL

✅

MySQL Connection Test

✅

Dynamic Schema Explorer

✅

Sample Data Explorer

✅

AI Database Guide

✅

SQL Error Correction

✅

Query History

✅

Query Result Table

✅

AI Result Explanation

✅

AI Chart Recommendation

✅

Matplotlib Visualization

✅

Seaborn Visualization

✅

Multiple Chart Types

✅

🚧 Future Improvements

Authentication and user management

Role-based database access

Query caching

SQL validation before execution

PostgreSQL support

SQL Server support

Conversation memory

Query performance monitoring

Production-grade security

Advanced dashboard generation

RAG-based schema/document retrieval using embeddings and a vector database

🎓 Learning Outcomes

This project provided practical experience with:

Large Language Models

Prompt Engineering

Text-to-SQL

Natural Language Processing

SQL

Relational Databases

SQLite

MySQL

Python

Pandas

Streamlit

API Integration

Data Visualization

Error Handling

Dynamic Schema Retrieval

AI-assisted Data Analysis

🎯 Project Objective

The goal of this project is to bridge the gap between non-technical users and relational databases.

Instead of requiring users to understand SQL syntax, the system allows them to ask questions in natural language and receive:

Natural Language Question
          ↓
       SQL Query
          ↓
     Database Result
          ↓
   AI Business Insight
          ↓
      Visualization

This makes database analytics more accessible, interactive, and user-friendly.

👨‍💻 Author

Rabi Ali

Data Science / AI Project

⭐ Conclusion

AI Analytics Assistant demonstrates how Large Language Models can be integrated with relational databases to create a natural-language analytics interface.

The project combines:

LLM + Text-to-SQL + Database Connectivity + Error Correction + Data Analysis + Visualization

into a single interactive application.
