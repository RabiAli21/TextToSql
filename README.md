# AI Analytics Assistant — Natural Language to SQL

An AI powered analytics assistant that allows users to interact with SQLite and MySQL databases using natural language instead of manually writing SQL.

## Project Overview

The application converts a user's natural-language question into SQL using an LLM through the Groq API, executes the query against the selected database, displays the result, corrects SQL errors when possible, generates AI insights, and recommends suitable visualizations.

### Example

**User question:**

> What is the total MRR by industry?

The application:

1. Retrieves the database schema.
2. Sends the schema and question to the AI.
3. Generates SQL.
4. Executes the SQL.
5. Displays the result.
6. Attempts automatic SQL correction if execution fails.
7. Generates an AI explanation.
8. Recommends and generates an appropriate chart.

## Features

- Natural Language to SQL
- SQLite support
- MySQL support
- MySQL connection testing
- Dynamic Schema Explorer
- AI Database Guide
- Automatic SQL Error Correction
- Query Result Display
- AI Result Analysis
- AI-Powered Visualization
- Query History
- Bar, Line, Scatter, Histogram, and Pie charts

## System Architecture

```text
                    User Question
                          |
                          v
                    Streamlit UI
                          |
                          v
                       Groq API
                          |
                          v
              Schema + User Question
                          |
                          v
                    SQL Generation
                          |
                          v
                 SQLite / MySQL
                          |
                          v
                   Query Result
                          |
             +------------+------------+
             |            |            |
             v            v            v
        AI Analysis   AI Chart     Result Table
                       Selection
                          |
                          v
                   Matplotlib /
                     Seaborn
```

## Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| AI / LLM | Groq API |
| AI Model | `openai/gpt-oss-120b` |
| LLM Client | OpenAI Python SDK |
| Web Framework | Streamlit |
| Databases | SQLite, MySQL |
| Data Processing | Pandas |
| Visualization | Matplotlib, Seaborn |
| Environment Variables | python-dotenv |
| MySQL Connector | mysql-connector-python |
| Version Control | Git / GitHub |

## Project Structure

```text
TextToSql/
|
+-- app.py
+-- sql.py
+-- revanstack.db
+-- .env
+-- .gitignore
+-- README.md
|
+-- dataset/
    +-- ravenstack_accounts.csv
    +-- ravenstack_churn_events.csv
    +-- ravenstack_feature_usage.csv
    +-- ravenstack_subscriptions.csv
    +-- ravenstack_support_tickets.csv
```

`app1.py` is the Groq-powered application.

## Environment Variables

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your API key to GitHub.

Add `.env` to `.gitignore`:

```text
.env
```

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TextToSql
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install streamlit pandas matplotlib seaborn python-dotenv mysql-connector-python openai
```

### 4. Add the Groq API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Run the Application

```bash
streamlit run app1.py
```

## Example Questions

### Account Analysis

```text
How many accounts are there?
```

```text
Show the number of accounts by industry.
```

```text
Which country has the most accounts?
```

### Revenue Analysis

```text
What is the total MRR?
```

```text
What is the total MRR by industry?
```

```text
Which industry generates the highest MRR?
```

```text
Show MRR by month.
```

### Customer Analysis

```text
How many customers have churned?
```

```text
Show the churn count by reason.
```

```text
Which customer segment has the highest churn?
```

### Support Analysis

```text
How many support tickets are there?
```

```text
Show support tickets by priority.
```

```text
Which category has the most support tickets?
```

### Feature Usage

```text
Which features are used the most?
```

```text
Show average feature usage by account.
```

## Application Workflow

```text
1. User enters a question
             |
             v
2. Application retrieves database schema
             |
             v
3. Question + schema sent to Groq
             |
             v
4. AI generates SQL
             |
             v
5. SQL displayed to the user
             |
             v
6. Query executed
             |
             v
7. If error -> AI corrects SQL
             |
             v
8. Result displayed as a DataFrame
             |
             v
9. AI analyzes the result
             |
             v
10. AI recommends a visualization
             |
             v
11. Matplotlib/Seaborn generates chart
```

## Prompt Engineering

The project uses schema-aware prompting.

The AI receives:

```text
Database Type
       +
Database Schema
       +
User Question
```

The model is instructed to:

- Use only existing tables.
- Use only existing columns.
- Follow the selected database dialect.
- Return only SQL for SQL-generation tasks.
- Avoid inventing database objects.
- Format generated SQL clearly.

This helps reduce invalid table and column names.

## Automatic SQL Error Correction

When generated SQL fails, the application sends the relevant information back to the AI.

```text
Generated SQL
      |
      v
Execute Query
      |
      v
   Error?
      |
      v
Schema + Question + SQL + Error
      |
      v
     Groq
      |
      v
Corrected SQL
      |
      v
Execute Again
```

This allows the application to recover from many common SQL-generation errors automatically.

## AI-Powered Visualization

The AI receives the user's question, SQL query, result columns, and sample result data.

It can recommend:

- Bar chart
- Line chart
- Scatter plot
- Histogram
- Pie chart
- No chart when visualization is not meaningful

### Example

```text
Question:
Total MRR by industry

AI Recommendation:
Bar Chart

X-axis -> Industry
Y-axis -> Total MRR
```

The application validates the recommendation before generating the chart.

## Schema Explorer

The Schema Explorer provides:

- Table names
- Row counts
- Column counts
- Column names
- Data types
- NULL / NOT NULL information
- Primary-key information
- Sample data

The explorer works with both SQLite and MySQL.

## AI Database Guide

The AI Database Guide analyzes the selected database structure and explains:

1. What the database appears to contain.
2. What each table represents.
3. Important columns.
4. Possible relationships.
5. Potential business analysis.
6. Useful questions.
7. Basic data-quality considerations.

## AI Result Analysis

After a query executes successfully, the application sends the result to the AI and generates a concise explanation based on the returned data.

The analysis is intended to focus on findings present in the query result rather than inventing unsupported conclusions.

## Query History

The sidebar stores questions asked during the current Streamlit session.

Example:

```text
Query History

1. Total MRR by industry
2. Number of accounts by country
3. Average subscription value
4. Total support tickets
```

## Security

API credentials are loaded from environment variables:

```python
os.getenv("GROQ_API_KEY")
```

Do not hard-code API keys in source code.

Do not commit `.env` to GitHub.

## Current Capabilities

| Feature | Status |
|---|---|
| Natural Language -> SQL | Complete |
| Groq Integration | Complete |
| SQLite | Complete |
| MySQL | Complete |
| MySQL Connection Test | Complete |
| Dynamic Schema Explorer | Complete |
| Sample Data Explorer | Complete |
| AI Database Guide | Complete |
| SQL Error Correction | Complete |
| Query History | Complete |
| Query Result Table | Complete |
| AI Result Explanation | Complete |
| AI Chart Recommendation | Complete |
| Matplotlib Visualization | Complete |
| Seaborn Visualization | Complete |
| Multiple Chart Types | Complete |

## Future Improvements

- Authentication and user management
- Role-based database access
- Query caching
- SQL validation before execution
- PostgreSQL support
- SQL Server support
- Conversation memory
- Query performance monitoring
- Production-grade security
- Advanced dashboard generation
- RAG-based schema and document retrieval using embeddings and a vector database

## Learning Outcomes

This project provided practical experience with:

- Large Language Models
- Prompt Engineering
- Text-to-SQL
- Natural Language Processing
- SQL
- Relational Databases
- SQLite
- MySQL
- Python
- Pandas
- Streamlit
- API Integration
- Data Visualization
- Error Handling
- Dynamic Schema Retrieval
- AI-assisted Data Analysis

## Project Objective

The goal of this project is to bridge the gap between non-technical users and relational databases.

Instead of requiring users to understand SQL syntax, the system allows them to ask questions in natural language and receive:

```text
Natural Language Question
          |
          v
       SQL Query
          |
          v
     Database Result
          |
          v
   AI Business Insight
          |
          v
      Visualization
```

This makes database analytics more accessible, interactive, and user-friendly.

## Author

**Rabi Ali**

Data Science / AI Project

## Conclusion

AI Analytics Assistant demonstrates how Large Language Models can be integrated with relational databases to create a natural-language analytics interface.

The project combines:

**LLM + Text-to-SQL + Database Connectivity + Error Correction + Data Analysis + Visualization**

into a single interactive application.
