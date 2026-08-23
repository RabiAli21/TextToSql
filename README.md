# 🤖 Text-to-SQL AI Expert

A simple **Text-to-SQL application** that converts natural language questions into SQL queries using Google's Gemini API and executes those queries on a SQLite database.

The goal of this project is to allow users to interact with structured data using normal English instead of writing SQL manually.

## 🚀 Features

* Convert natural language questions into SQL queries
* Uses Google Gemini for SQL generation
* SQLite database integration
* Automatically reads database tables and columns
* Executes generated SQL queries
* Displays query results through a Streamlit interface
* Supports multiple CSV datasets
* Dynamic database schema handling

## 🛠️ Technologies Used

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
├── .gitignore
├── README.md
│
├── dataset/
│   └── *.csv
│
└── .env
```

> `.env`, `revanstack.db`, and `venv/` should not be uploaded to GitHub.

## ⚙️ How It Works

```text
User Question
      ↓
Streamlit Interface
      ↓
Database Schema
      ↓
Gemini API
      ↓
Generated SQL Query
      ↓
SQLite Database
      ↓
Query Result
      ↓
Streamlit
```

### Example

User asks:

```text
How many customers are there?
```

Gemini generates:

```sql
SELECT COUNT(*) FROM customers;
```

The query is then executed against the SQLite database and the result is displayed in the application.

## 📋 Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install streamlit pandas python-dotenv google-generativeai
```

## 🔑 API Key Setup

Create a `.env` file in the project directory:

```text
GOOGLE_API_KEY=your_google_api_key
```

Never upload your `.env` file or API key to GitHub.

## 🗄️ Create the Database

The `sql.py` file loads CSV files from the `dataset` folder into SQLite tables.

Run:

```bash
python sql.py
```

This creates:

```text
revanstack.db
```

## ▶️ Run the Application

Start Streamlit with:

```bash
streamlit run app.py
```

Then open the local URL provided by Streamlit.

## 💡 Example Questions

You can ask questions such as:

* How many records are in the table?
* What is the average value?
* Show the top 5 records.
* Which category has the highest sales?
* What is the total sales amount?
* Show customers from Jaipur.
* Which product has the highest price?

The application converts these questions into SQL automatically.

## 🔐 Security

The Google API key is stored in `.env` and should never be committed to GitHub.

The `.gitignore` file excludes:

```text
.env
venv/
__pycache__/
*.pyc
revanstack.db
```

## 🔮 Future Improvements

* Add SQL query display in the UI
* Add charts and visualizations
* Add conversation history
* Improve error handling
* Add support for more database systems
* Add query validation before execution
* Add natural-language explanations of SQL results

## 👨‍💻 Author

**Rabi Ali**

Data Science | Data Analytics | AI & Machine Learning

---

⭐ If you find this project useful, consider giving the repository a star!
