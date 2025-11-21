# 🤖 Text-to-SQL/NoSQL LLM Application

A powerful Natural Language to SQL/MongoDB Query Generator powered by **Llama 3.2** running locally via Ollama. This application allows users to ask questions in plain English and automatically generates queries to retrieve data from both **SQLite** and **MongoDB** databases.

## ✨ Features

- 🔍 **Natural Language Processing**: Convert plain English questions to SQL/MongoDB queries
- 🚀 **Local LLM**: Uses Llama 3.2 via Ollama (no API costs, complete privacy)
- 📊 **Dual Database Support**: Works with both SQLite and MongoDB
- 💾 **Database Management**: Pre-populated with 30+ student records
- 🔄 **Database Switching**: Easily toggle between SQLite and MongoDB
- 📈 **Interactive UI**: Built with Streamlit for easy interaction
- 📥 **Export Results**: Download query results as CSV
- 🎨 **Clean Interface**: Modern UI with example queries and schema display

## 🛠️ Technologies Used

- **Python 3.x**
- **Streamlit** - Web interface
- **Ollama** - Local LLM runtime
- **Llama 3.2** - Language model
- **SQLite** - Relational database
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver
- **Pandas** - Data manipulation
- **Requests** - API communication

## 📋 Prerequisites

Before running this application, ensure you have:

1. **Python 3.8+** installed
2. **Ollama** installed ([Download here](https://ollama.com/download))
3. **MongoDB** installed ([Download here](https://www.mongodb.com/try/download/community)) or use MongoDB Compass

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd "Text to sql llm application"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Create a `requirements.txt` file with:
```
streamlit==1.31.0
pandas==2.1.4
python-dotenv==1.0.0
requests==2.31.0
pymongo==4.6.0
```

### 3. Install and Setup Ollama

**Download Ollama:**
- Visit [ollama.com/download](https://ollama.com/download)
- Install for your operating system

**Pull Llama 3.2 Model:**
```bash
ollama pull llama3.2
```

**Start Ollama Server:**
```bash
ollama serve
```

### 4. Install and Setup MongoDB

**Download MongoDB:**
- Visit [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
- Install for your operating system
- MongoDB will run as a service automatically

**Or use MongoDB Compass (GUI):**
- Download from [mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
- Connect to `mongodb://localhost:27017`

### 5. Setup Databases

**Setup SQLite:**
```bash
python sqlite.py
```

**Setup MongoDB:**
```bash
python mongodb.py
```

This creates both `Student.db` (SQLite) and populates MongoDB `text_to_sql` database with 30 student records.

## 🎯 Usage

### 1. Start MongoDB (if not running automatically)

MongoDB usually runs as a service. Verify it's running by opening MongoDB Compass and connecting to `mongodb://localhost:27017`

### 2. Start Ollama (if not already running)

```bash
ollama serve
```

### 3. Run the Streamlit Application

```bash
streamlit run sql.py
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

### 5. Select Database Type

In the sidebar, choose between:
- **SQLite** - Relational database with SQL queries
- **MongoDB** - NoSQL database with MongoDB queries

### 6. Ask Questions

Enter questions in plain English, such as:
- "List all students in class 8th"
- "How many students are in section A?"
- "Show names of students who scored more than 90 marks"
- "Find students from New York with attendance above 90%"
- "What is the average attendance of 9th class students?"
- "Display all students"

## 📊 Database Schema

**SQLite Schema:**
```sql
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
```

**MongoDB Schema:**
```json
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
```

## 📁 Project Structure

```
Text to sql llm application/
│
├── sql.py              # Main Streamlit application
├── sqlite.py           # SQLite database setup
├── mongodb.py          # MongoDB database setup
├── reset_mongodb.py    # Reset MongoDB data
├── test_mongo.py       # Test MongoDB connection
├── Student.db          # SQLite database (generated)
├── .env                # Environment variables (optional)
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file for configuration:

```env
MONGO_URI=mongodb://localhost:27017/
DEEPSEEK_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

### Model Selection

To use a different Ollama model, modify `sql.py`:

```python
response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'llama3.2',  # Change to: llama3.2:1b, qwen2.5:3b, etc.
        ...
    }
)
```

## 💡 Example Queries

| Question | Generated SQL |
|----------|--------------|
| "List all students in class 8th" | `SELECT * FROM STUDENT WHERE CLASS = '8th';` |
| "How many students are in section A?" | `SELECT COUNT(*) FROM STUDENT WHERE SECTION = 'A';` |
| "Show top 5 students by marks" | `SELECT * FROM STUDENT ORDER BY MARKS DESC LIMIT 5;` |
| "Find students from New York" | `SELECT * FROM STUDENT WHERE CITY = 'New York';` |

**MongoDB Query Examples:**

| Question | Generated MongoDB Query |
|----------|------------------------|
| "List all students in class 8th" | `{"class": "8th"}` |
| "Show students who scored more than 90" | `{"marks": {"$gt": 90}}` |
| "Find students from New York" | `{"city": "New York"}` |
| "Display all students" | `{}` |

## 🐛 Troubleshooting

### Ollama Connection Error
**Error:** `❌ Cannot connect to Ollama`

**Solution:**
```bash
# Make sure Ollama is running
ollama serve
```

### MongoDB Connection Error
**Error:** `Cannot connect to MongoDB`

**Solution:**
```bash
# Check if MongoDB is running
# Open MongoDB Compass and connect to mongodb://localhost:27017
# Or start MongoDB service (Windows):
net start MongoDB
```

### Database Not Found (SQLite)
**Error:** `Database Error: no such table: STUDENT`

**Solution:**
```bash
# Run the database setup script
python sqlite.py
```

### MongoDB No Data
**Error:** `No results found` in MongoDB

**Solution:**
```bash
# Reset and reload MongoDB data
python mongodb.py
```

### Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Run on a different port
streamlit run sql.py --server.port 8502
```

## 🎨 Features Overview

### 1. **Dual Database Support**
- SQLite for relational queries
- MongoDB for NoSQL queries
- Easy switching between databases

### 2. **Query Generation**
- Converts natural language to SQL/MongoDB queries
- Supports complex queries with filtering, aggregations, and sorting
- Automatic query correction

### 3. **Results Display**
- Clean table format with Pandas DataFrames
- Column headers
- Export to CSV
- Success/error indicators

### 4. **Database Stats**
- Total student count
- Number of classes
- Number of subjects

### 5. **Example Questions**
- Built-in examples to help users get started
- Covers common query patterns
- Database-specific examples

## 🔒 Privacy & Security

- ✅ Runs 100% locally - no data sent to external servers
- ✅ No API keys required (when using Ollama)
- ✅ Complete data privacy
- ✅ No usage limits or costs
- ✅ Supports both SQL and NoSQL databases

## 🚀 Future Enhancements

- [ ] Support for PostgreSQL, MySQL
- [ ] Query history and favorites
- [ ] Visual query builder
- [ ] Chart/graph generation from results
- [ ] Multi-language support
- [ ] Voice input for queries
- [ ] Query optimization suggestions
- [ ] Real-time collaboration
- [ ] Database performance monitoring

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Ramsaheb Prasad**

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Happy Querying! 🎉**