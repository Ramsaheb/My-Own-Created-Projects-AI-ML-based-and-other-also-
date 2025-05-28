# 📰 Media Pulse Dashboard

### Track public perception of brands, topics, and personalities in real time.

---

## 📌 Project Summary

**Media Pulse Dashboard** is an internal sentiment analysis tool designed for PR teams to monitor how brands, topics, and public figures are perceived across news media. The dashboard fetches recent articles, performs sentiment analysis, and displays the results in a visually intuitive way. 

Example topics include: *Apple, Elon Musk, Finance Trends, SpaceTech, Nike Sustainability*, etc.

---

## 🛠️ Stack Used

| Layer        | Technology                             |
|--------------|--------------------------------------|
| Frontend     | **Flask** (used to render the UI)    |
| Backend      | **Next.js** (handles API and NLP logic) |
| Sentiment API| **HuggingFace Transformers**         |
| News API     | **[NewsAPI.org](https://newsapi.org/)** |
| Hosting      | **Replit (for testing only)**         |

---

## 🚀 Features

- 🔍 Enter a keyword or topic to analyze  
- 📰 Fetches related news headlines  
- 🧠 Performs sentiment analysis (Positive / Neutral / Negative)  
- ✍️ Summarizes each article in 2 lines  
- 🌐 Displays article source and publication date  
- 📊 Visual stats showing distribution of sentiments  
- ✅ Simple and easy-to-use interface  

---

## 📂 Folder Structure

```plaintext
Project structure of 'media-pulse-dashboard':
📁 .config/
📄 .env
📁 .git/
📄 .gitignore
📄 .replit
📁 backend/
  📄 config.py
  📄 main.py
  📄 mock_articles.json
  📄 news_service.py
  📄 requirements.txt
  📄 sentiment.py
📁 frontend/
  📄 .env.local
  📁 components/
    📄 ArticleCard.jsx
    📄 Dashboard.jsx
    📄 Header.jsx
    📄 Loader.jsx
    📄 SearchBar.jsx
    📄 SentimentFilter.jsx
    📄 StatsCard.jsx
  📁 pages/
    📄 index.js
    📄 _app.js
  📁 services/
    📄 api.js
  📁 styles/
    📄 animations.css
    📄 main.css
    📄 variables.css
📄 next.config.js
📄 package-lock.json
📄 package.json
📄 pyproject.toml
📄 README.md
📄 replit.nix
📄 uv.lock
```
---
## 🧠 AI Feature Explanation
✅ Sentiment Analysis
Analysis is performed through an authenticated API call using a HuggingFace token

✅ Article Summarization
Summaries are limited to 2 lines for clarity

Summaries are either truncated or mock-generated due to resource limits

---
## ⚙️ Setup Instructions
🔧 Backend (Flask)

Run the following commands:

```bash
cd backend
pip install -r requirements.txt
python main.py
```
🌐 Frontend (Next js)

Run the following commands:

```bash
cd frontend
npm install
npm run dev
```
---
## 🧪 Replit Deployment Notes
The project runs on Replit’s testing server, which is not suitable for production or development purposes.

⚠️ Important: Do not install any packages other than those listed in requirements.txt and package.json.

Replit has limited storage, and installing additional packages may cause "storage full" errors.

---
## ❗ Limitations & Known Issues
Sentiment and News APIs use free-tier limits and may throttle requests

Replit’s environment can become unstable with additional installs

No persistent database; all articles are stored in memory

