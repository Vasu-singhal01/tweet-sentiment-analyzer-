import json
import os
import random
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

# Simulated tweet templates.
TEMPLATES = {
    "positive": [
        "Just tried {kw} and honestly blown away. So much better than expected!",
        "Can't stop talking about {kw} - it's a total game changer this year.",
        "{kw} just solved a problem I've had for years. Highly recommend it.",
        "Massive shoutout to the {kw} team. This is incredible work.",
        "{kw} actually exceeded all my expectations. Brilliant stuff.",
        "Using {kw} every day now. Life is genuinely better because of it.",
        "The latest {kw} update is exactly what we needed. Love it.",
        "{kw} is the best thing to happen in tech this year. Amazing work.",
        "Wow, {kw} is just outstanding. Everyone should try this.",
        "Happy to say {kw} is finally working perfectly. Great job team!",
    ],
    "negative": [
        "Really disappointed with {kw} lately. The quality has gone downhill badly.",
        "Spent 2 hours dealing with {kw} issues today. Absolutely frustrating.",
        "{kw} keeps crashing on me. Not acceptable at this point at all.",
        "Why is {kw} still so slow? Someone needs to fix this already.",
        "{kw} was great before. Now it's just terrible. What happened?",
        "The {kw} experience is getting worse with every update. Avoid it.",
        "Wasted my money on {kw}. Horrible experience from start to finish.",
        "{kw} is a disaster. Nothing works as advertised. Very disappointed.",
    ],
    "neutral": [
        "{kw} just released a new version. Here is what changed in this update.",
        "Researchers published a new study on the impact of {kw} today.",
        "{kw} is trending globally on social media right now.",
        "A quick overview of {kw} for anyone who is new to this topic.",
        "According to latest reports, {kw} usage has grown significantly.",
        "{kw} is now available across multiple platforms worldwide.",
        "New analysis of {kw} shows interesting patterns in user behavior.",
    ],
}

DEFAULT_XQUIK_SEARCH_URL = "https://xquik.com/api/v1/x/tweets/search"
DEFAULT_XQUIK_LIMIT = 18


def generate_tweets(keyword: str) -> list[dict]:
    """Generate simulated tweets for the given keyword."""
    tweets = []
    counts = {
        "positive": 7 + random.randint(0, 4),
        "negative": 3 + random.randint(0, 4),
        "neutral": 3 + random.randint(0, 3),
    }
    for category, n in counts.items():
        tmpl_list = TEMPLATES[category]
        for i in range(n):
            text = tmpl_list[i % len(tmpl_list)].replace("{kw}", keyword)
            tweets.append({"text": text, "category": category})
    random.shuffle(tweets)
    return tweets


def tweet_text(tweet: object) -> str | None:
    """Extract tweet text from a normalized API record."""
    if not isinstance(tweet, dict):
        return None

    for key in ("text", "fullText", "full_text"):
        value = tweet.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return None


def fetch_xquik_tweets(keyword: str, limit: int = DEFAULT_XQUIK_LIMIT) -> list[dict]:
    """Fetch live tweets from Xquik when an API key is configured."""
    api_key = os.environ.get("XQUIK_API_KEY", "").strip()
    if not api_key:
        return []

    search_url = os.environ.get("XQUIK_SEARCH_URL", DEFAULT_XQUIK_SEARCH_URL).strip()
    query = urlencode(
        {
            "q": keyword,
            "queryType": "Latest",
            "limit": max(1, min(limit, 100)),
        }
    )
    request = Request(
        f"{search_url}?{query}",
        headers={
            "Accept": "application/json",
            "x-api-key": api_key,
        },
    )

    try:
        with urlopen(request, timeout=8) as response:
            payload = json.load(response)
    except (OSError, URLError, ValueError):
        return []

    if not isinstance(payload, dict):
        return []

    tweets = payload.get("tweets")
    if not isinstance(tweets, list):
        return []

    live_tweets = []
    for tweet in tweets:
        text = tweet_text(tweet)
        if text:
            live_tweets.append({"text": text, "category": "live"})

    return live_tweets


def tweets_for_keyword(keyword: str) -> tuple[list[dict], str]:
    """Use live tweets when available, otherwise keep the local sample flow."""
    live_tweets = fetch_xquik_tweets(keyword)
    if live_tweets:
        return live_tweets, "xquik"

    return generate_tweets(keyword), "sample"


def analyze_tweets(tweets: list[dict]) -> list[dict]:
    """Run VADER sentiment analysis on each tweet."""
    results = []
    for tweet in tweets:
        scores = analyzer.polarity_scores(tweet["text"])
        compound = scores["compound"]  # -1.0 to +1.0

        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        confidence = round(abs(compound) * 0.5 + 0.5, 2)  # map to 0.5-1.0 range

        results.append(
            {
                "text": tweet["text"],
                "label": label,
                "compound": round(compound, 3),
                "positive": round(scores["pos"], 3),
                "negative": round(scores["neg"], 3),
                "neutral": round(scores["neu"], 3),
                "confidence": confidence,
            }
        )
    return results


# Routes.


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    keyword = data.get("keyword", "").strip()
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    tweets, source = tweets_for_keyword(keyword)
    results = analyze_tweets(tweets)

    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in results:
        counts[r["label"]] += 1

    total = len(results)
    dominant = max(counts, key=counts.get)
    avg_conf = round(sum(r["confidence"] for r in results) / total * 100)
    trend_data = [
        max(5, min(95, (counts["Positive"] / total * 100) + random.randint(-20, 20)))
        for _ in range(8)
    ]

    return jsonify(
        {
            "keyword": keyword,
            "source": source,
            "total": total,
            "counts": counts,
            "dominant": dominant,
            "avg_conf": avg_conf,
            "tweets": results[:6],  # top 6 for display
            "trend": [round(v) for v in trend_data],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
