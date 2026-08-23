# 🤖 AI-Powered Text-to-SQL Analytics Assistant

An AI-powered **Text-to-SQL Analytics Assistant** that allows users to ask questions about structured data in natural language. The application uses **Google Gemini** to convert user questions into SQL queries, executes them on a **SQLite database**, handles SQL errors with automatic query correction, and presents the results with interactive visualizations.

## 🚀 Live Demo

🔗 **Streamlit App:**  [text-to-mysql.streamlit.app](https://text-to-mysql.streamlit.app/)

## ✨ Features

* 🗣️ Ask database questions using natural language
* 🤖 Generate SQL queries using Google Gemini
* 🗄️ Automatically use the database schema
* 🔍 Display the generated SQL query
* ⚡ Execute SQL queries on SQLite
* 🛠️ Automatically detect and correct SQL errors
* 📊 Display query results as interactive tables
* 📈 Automatically generate visualizations for suitable query results
* 🌐 Streamlit web interface
* 📁 Supports CSV-based datasets

## 🧠 How It Works

```text
User Question
      ↓
Database Schema
      ↓
Google Gemini
      ↓
SQL Query Generation
      ↓
SQL Validation & Execution
      ↓
   ┌───────────────┐
   │               │
 Success         Error
   │               │
   ↓               ↓
Result        Gemini Correction
   │               │
   │               ↓
   │           Corrected SQL
   │               │
   └───────→ SQLite Database
                   ↓
             Query Results
                   ↓
          Table + Visualization
```

## 🛠️ Tech Stack

* **Python**
* **Google Gemini API**
* **SQLite**
* **Pandas**
* **Streamlit**
* **python-dotenv**

## 📂 Project Structure

```text
TextToSql/
│
├── app.py
├── sql.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── dataset/
│   └── *.csv
│
├── revanstack.db
└── .env
```

> `.env` should never be uploaded to GitHub.

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TextToSql
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 API Key Configuration

Create a `.env` file in the project directory:

```text
GOOGLE_API_KEY=your_google_api_key
```

The application reads the API key using `python-dotenv`.

**Never commit your `.env` file or expose your API key publicly.**

## 🗄️ Database

The project uses **SQLite** as its database.

The `sql.py` script loads CSV files from the `dataset` folder and converts them into SQLite tables.

Run:

```bash
python sql.py
```

This creates/updates:

```text
revanstack.db
```

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 💬 Example Questions

You can ask questions such as:

```text
What are the top 5 active accounts?

What is the total revenue?

Which customers have the highest spending?

Show the average revenue by category.

What are the top 10 products?

How many active customers are there?
```

The application converts the natural-language question into SQL and executes it against the database.

## 📊 Query Result & Visualization

The application displays:

1. **Generated SQL**
2. **Query Result**
3. **Automatic Visualization** when the result contains suitable categorical and numerical data

For example:

```text
User:
Top 5 accounts by MRR
        ↓
Gemini generates SQL
        ↓
SQLite executes SQL
        ↓
Result displayed as a table
        ↓
Bar chart generated automatically
```

## 🛠️ Automatic SQL Error Correction

If Gemini generates an invalid SQL query, the application captures the SQLite error and sends the following information back to Gemini:

* Original user question
* Database schema
* Generated SQL
* SQLite error

Gemini then generates a corrected SQL query and the application attempts to execute it again.

This creates a self-correction workflow:

```text
Generated SQL
      ↓
SQLite
      ↓
SQL Error
      ↓
Gemini
      ↓
Corrected SQL
      ↓
SQLite
      ↓
Result
```

## ☁️ Deployment

The application can be deployed using **Streamlit Cloud**.

For deployment:

1. Push the project to GitHub.
2. Connect the repository to Streamlit Cloud.
3. Set `app.py` as the main application file.
4. Add the required packages in `requirements.txt`.
5. Add your Google API key to Streamlit Cloud Secrets.

Example secret:

```toml
GOOGLE_API_KEY = "your_google_api_key"
```

## 📦 Requirements

The main dependencies are:

```text
streamlit
pandas
python-dotenv
google-generativeai
```

## 🔐 Security

Sensitive credentials should never be committed to GitHub.

The `.gitignore` file should include:

```text
.env
venv/
__pycache__/
*.pyc
```

## 🔮 Future Improvements

* Add query history
* Support multiple database types such as MySQL and PostgreSQL
* Add advanced chart recommendations
* Add conversational follow-up questions
* Add authentication
* Improve SQL validation and security
* Add downloadable query results
* Add dashboard generation from natural-language questions

## 👨‍💻 Author

**Rabi Ali**

Data Science | Data Analytics | AI & Machine Learning

---

⭐ If you find this project useful, consider giving the repository a star!
