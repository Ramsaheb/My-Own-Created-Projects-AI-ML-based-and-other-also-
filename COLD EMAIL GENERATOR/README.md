
# 📧 Cold Email Generator

A sophisticated AI-powered cold email generator that creates personalized business emails by analyzing job postings and matching them with relevant portfolio projects.

## 🚀 Features

- **Web Scraping**: Extracts job information from job posting URLs
- **AI-Powered Analysis**: Uses Groq's LLM to analyze job requirements
- **Portfolio Matching**: Automatically matches relevant portfolio projects to job requirements
- **Professional Email Generation**: Creates personalized cold emails with portfolio links
- **Vector Database**: Uses ChromaDB for efficient portfolio search and matching
- **Streamlit Interface**: Clean, user-friendly web interface

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/LLM**: Groq (Llama model)
- **Vector Database**: ChromaDB
- **Web Scraping**: LangChain WebBaseLoader, BeautifulSoup
- **Data Processing**: Pandas

## 📋 Prerequisites

- Python 3.11+
- Groq API Key

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cold-email-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the `COLD EMAIL GENERATOR/app/` directory:
   ```env
   Groq_API_KEY=your_groq_api_key_here
   ```

## 🚀 Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Access the web interface**:
   Open your browser and navigate to the provided URL (typically `http://localhost:5000`)

3. **Generate cold emails**:
   - Enter a job posting URL
   - Click "Submit"
   - The system will analyze the job requirements and generate a personalized cold email

## 📁 Project Structure

```
COLD EMAIL GENERATOR/
├── app/
│   ├── resource/
│   │   └── my_portfolio.csv      # Portfolio data
│   ├── vectorstore/              # ChromaDB vector storage
│   ├── main.py                   # Streamlit application
│   ├── chains.py                 # LLM chains and prompts
│   ├── portfolio.py              # Portfolio management
│   └── utils.py                  # Utility functions
├── main.py                       # Application entry point
└── README.md                     # Project documentation
```

## ⚙️ Configuration

### Portfolio Setup

Update the `my_portfolio.csv` file with your portfolio projects:

```csv
Techstack,Links
"React, Node.js, MongoDB",https://example.com/react-portfolio
"Python, Django, MySQL",https://example.com/python-portfolio
```

### Environment Variables

- `Groq_API_KEY`: Your Groq API key for LLM access

## 🔍 How It Works

1. **URL Processing**: Takes a job posting URL as input
2. **Content Extraction**: Scrapes job description and requirements
3. **AI Analysis**: Uses Groq LLM to extract key information:
   - Job title and company
   - Required skills
   - Responsibilities
   - Qualifications
4. **Portfolio Matching**: Searches vector database for relevant portfolio projects
5. **Email Generation**: Creates personalized cold email highlighting relevant experience

## 📧 Email Template

The generated emails include:
- Professional introduction from "Mohan" at AtliQ
- Company overview and services
- Relevant portfolio project highlights
- Call-to-action for meeting/call

## 🎯 Example Usage

```python
# Example job posting URL
url = "https://company.com/job-posting"

# The system will generate an email like:
"""
Subject: AtliQ - Perfect Match for Your [Job Title] Position

Dear Hiring Manager,

I'm Mohan, a business development executive at AtliQ...
[Personalized content based on job requirements]
[Relevant portfolio links]

Best regards,
Mohan
AtliQ Team
"""
```

## 🔧 Customization

### Adding New Portfolio Projects

1. Update `my_portfolio.csv` with new entries
2. Restart the application to load new data into the vector database

### Modifying Email Templates

Edit the prompts in `chains.py` to customize email tone and structure.

## 🐛 Troubleshooting

### Common Issues

1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **API Key Issues**: Ensure your Groq API key is correctly set in `.env`
3. **Port Conflicts**: The app runs on port 5000 by default

### Logs and Debugging

Check the console output for error messages and debugging information.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Groq](https://groq.com/) for the LLM API
- [LangChain](https://langchain.com/) for the framework
- [Streamlit](https://streamlit.io/) for the web interface
- [ChromaDB](https://www.trychroma.com/) for vector storage

## 📞 Support

For support and questions, please open an issue in the repository.

---

**Built with ❤️ using AI and modern web technologies**
