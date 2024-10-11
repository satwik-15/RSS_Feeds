import feedparser
import pandas as pd
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

nltk.download('punkt')
nltk.download('stopwords')

categories = ["Terrorism / protest / political unrest / riot", "Positive/Uplifting", "Natural Disasters", "Others"]
rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    filtered_tokens = [w for w in tokens if w.isalpha() and w.lower() not in stop_words]
    return ' '.join(filtered_tokens)

def fetch_and_parse_rss(feeds):
    articles = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            articles.append({
                "title": entry.title if 'title' in entry else None,
                "content": entry.summary if 'summary' in entry else None,
                "publication_date": entry.published if 'published' in entry else None,
                "source": feed
            })
    return articles

def categorize_article(article):
    text = article.lower()
    if any(keyword in text for keyword in ["protest", "terror", "political", "riot", "unrest"]):
        return "Terrorism / protest / political unrest / riot"
    elif any(keyword in text for keyword in ["happy", "joy", "positive", "uplifting", "good news"]):
        return "Positive/Uplifting"
    elif any(keyword in text for keyword in ["earthquake", "flood", "disaster", "hurricane", "fire", "natural disaster"]):
        return "Natural Disasters"
    else:
        return "Others"

articles = fetch_and_parse_rss(rss_feeds)

for article in articles:
    article['category'] = categorize_article(article['content'] if article['content'] else article['title'])

df = pd.DataFrame(articles)

output_file = "rss_feed_articles.xlsx"
df.to_csv(output_file, index=False)

output_file
