from textblob import TextBlob
import requests

def get_sentiment(news_text):
    analysis = TextBlob(news_text)
    return "Positive" if analysis.sentiment.polarity > 0 else "Negative"

# Example usage:
news = "Stock market is booming with record highs!"
print(get_sentiment(news))