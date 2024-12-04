import requests
from difflib import SequenceMatcher
from typing import Dict, Optional, List

# API key for the NewsData API
API_KEY = "pub_61237c06f64f177491db90d43ed8a31a07ba9"

# List of trusted news sources
TRUSTED_SOURCES = [
    "bbc.com",
    "cnn.com",
    "reuters.com",
    "nytimes.com",
    "theguardian.com",
    "deadline.com",
]

class NewsFakeDetector:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_news_articles(self, query: str) -> Optional[Dict]:
        """
        Fetch news articles based on a query from NewsData API.
        """
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": self.api_key,
            "q": query,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return None

    def is_trusted_source(self, source_url: str) -> bool:
        """
        Check if the source URL belongs to a trusted source.
        """
        for trusted_source in TRUSTED_SOURCES:
            if trusted_source in source_url:
                return True
        return False

    def get_similarity(self, a: str, b: str) -> float:
        """
        Calculate the similarity ratio between two strings using SequenceMatcher.
        """
        return SequenceMatcher(None, a, b).ratio()

    def find_most_similar_title(self, query: str, articles: List[Dict]) -> Optional[Dict[str, float]]:
        """
        Find the article with the title most similar to the query.
        """
        similarity_scores = {
            article["title"]: self.get_similarity(query, article["title"])
            for article in articles if "title" in article
        }
        if not similarity_scores:
            return None
        most_similar_title = max(similarity_scores, key=similarity_scores.get)
        return {"title": most_similar_title, "score": similarity_scores[most_similar_title]}

    def detect_fake_news(self, query: str) -> List[Dict]:
        """
        Detect fake news by verifying the source of each article and finding similar articles.
        """
        articles = self.fetch_news_articles(query)
        if not articles or "results" not in articles:
            return []

        results = []
        for article in articles["results"]:
            source_url = article.get("link", "")
            is_trusted = self.is_trusted_source(source_url)
            status = "Real" if is_trusted else "Fake"
            results.append({
                "title": article.get("title", "No Title"),
                "description": article.get("description", "No Description"),
                "source": article.get("source_id", "Unknown Source"),
                "source_url": source_url,
                "status": status,
            })

        # Find the most similar article to the query
        most_similar = self.find_most_similar_title(query, articles["results"])
        if most_similar:
            print(f"Most Similar Article: {most_similar['title']}")
            print(f"Similarity Score: {most_similar['score']:.2f}")

        return results


# Main entry point for the command-line application
if __name__ == "__main__":
    detector = NewsFakeDetector(API_KEY)

    # Ask for user input
    query = input("Enter a topic or keyword to detect fake news: ").strip()
    if not query:
        print("No query provided. Exiting.")
    else:
        results = detector.detect_fake_news(query)
        if not results:
            print("No articles found.")
        else:
            print("\nDetection Results:")
            for article in results:
                print(f"\nTitle: {article['title']}")
                print(f"Description: {article['description']}")
                print(f"Source: {article['source']}")
                print(f"Source URL: {article['source_url']}")
                print(f"Status: {article['status']}")
