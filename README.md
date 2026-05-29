# 🐦 Tweet Sentiment Analyzer

A web-based NLP project that analyzes the sentiment of tweets for any keyword using **VADER** (Valence Aware Dictionary and sEntiment Reasoner) — a rule-based sentiment analysis tool specifically designed for social media text.

Built as a resume project for B.Tech CSE (Data Science).

---

## 🚀 Live Demo

> _Deploy on Render (free) and paste your link here_

---

## 📸 Features

- 🔍 Enter any keyword — get instant sentiment analysis
- 🤖 Real NLP using **VADER** (not just word counting)
- 📊 3 interactive charts: Donut, Bar, Line (trend)
- 🧠 Plain-English explanation of results
- 🐍 Python + Flask backend
- 💻 Clean dark-themed UI

---

## 🛠️ Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Python 3, Flask         |
| NLP       | VADER (vaderSentiment)  |
| Frontend  | HTML, CSS, JavaScript   |
| Charts    | Chart.js                |
| Fonts     | Google Fonts (Syne, Space Mono) |

---

## 📁 Project Structure

```
sentiment_analyzer/
│
├── app.py                  # Flask backend + VADER logic
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
└── templates/
    └── index.html          # Frontend UI
```

---

## ⚙️ How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/tweet-sentiment-analyzer.git
cd tweet-sentiment-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## 🧠 How It Works

### What is VADER?
VADER is a lexicon and rule-based sentiment analysis tool built for social media. It returns 4 scores for any text:
- **pos** — proportion of positive sentiment
- **neg** — proportion of negative sentiment
- **neu** — proportion of neutral sentiment
- **compound** — overall score from -1.0 (most negative) to +1.0 (most positive)

### Classification Logic
```python
if compound >= 0.05:   → Positive
if compound <= -0.05:  → Negative
else:                  → Neutral
```

### Flow
```
User enters keyword
      ↓
Flask generates simulated tweets using templates
      ↓
VADER analyzes each tweet → returns compound score
      ↓
Tweets classified as Positive / Negative / Neutral
      ↓
Results sent to frontend as JSON
      ↓
Chart.js renders 3 interactive charts
      ↓
Plain-English summary shown to user
```

---

## 🌐 Deploy for Free (Render)

1. Push this project to GitHub
2. Go to [https://render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click Deploy — you'll get a free live URL!

> Add `gunicorn` to requirements.txt before deploying:
> ```
> gunicorn==21.2.0
> ```

---

## 👤 Author

**Your Name**
B.Tech CSE (Data Science)
[LinkedIn](#) | [GitHub](#)

---

## 📄 License

MIT License — free to use and modify.
