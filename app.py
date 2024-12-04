from flask import Flask, request, jsonify, render_template
import requests
import json
from typing import Dict, Optional
from flask_cors import CORS  # Make sure to install flask-cors: pip install flask-cors

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API keys and URLs
MEDIASTACK_API_KEY = "pub_61237c06f64f177491db90d43ed8a31a07ba9"
GEMINI_API_KEY = "AIzaSyCcl8cEP604d8pvpDwH4a9MF5NX7Lkc6e0"
NEWSDATA_API_KEY = "pub_61237c06f64f177491db90d43ed8a31a07ba9"

MEDIASTACK_BASE_URL = "https://newsdata.io/api/1/news"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Trusted news sources for credibility check
TRUSTED_SOURCES = [
    "bbc.com",
    "cnn.com",
    "reuters.com",
    "nytimes.com",
    "theguardian.com",
    "deadline.com",
]

class NewsFakeDetector:
    def __init__(self):
        self.api_key = NEWSDATA_API_KEY

    def fetch_news_articles(self, query: str, language: str = "en") -> Optional[Dict]:
        params = {
            "apikey": self.api_key,
            "q": query,
            "language": language,
        }
        try:
            response = requests.get(MEDIASTACK_BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return None

    def is_trusted_source(self, source_url: str) -> bool:
        return any(trusted_source in source_url for trusted_source in TRUSTED_SOURCES)

    def detect_fake_news(self, query: str):
        articles = self.fetch_news_articles(query)
        if not articles or "results" not in articles:
            return []
        
        detailed_results = []
        formatted_results = []
        for article in articles["results"]:
            title = article.get("title", "No Title")
            source_url = article.get("source_url", "")
            source = article.get("source", "Unknown Source")
            description = article.get("description", "No Description")
            is_trusted = self.is_trusted_source(source_url)
            
            # Detailed result for frontend
            detailed_result = {
                "title": title,
                "source": source,
                "source_url": source_url,
                "description": description,
                "is_trusted": is_trusted
            }
            detailed_results.append(detailed_result)
            
            # Formatted string result
            formatted_result = f"Title: '{title}'\n"
            formatted_result += f"Source: {source} ({source_url})\n"
            
            if is_trusted:
                formatted_result += "-> Trusted Source ✅"
            else:
                formatted_result += "-> Untrusted Source ⚠\n"
                formatted_result += "-> No matching trusted content. 🚩 Potential Fake News"
            
            formatted_results.append(formatted_result)
        
        return detailed_results, formatted_results

# Initialize the news detector
detector = NewsFakeDetector()

@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")

@app.route("/handle_request", methods=["POST"])
def handle_request():
    """Handle news and article generation requests."""
    data = request.json
    if not data or "type" not in data or "input" not in data:
        return jsonify({"success": False, "error": "Invalid request parameters."}), 400

    if data["type"] == "news":
        return fetch_news(
            data["input"], 
            data.get("country"), 
            data.get("category")
        )
    elif data["type"] == "article":
        return generate_article(data["input"])
    elif data["type"] == "fake_news":
        detailed_results, formatted_results = detector.detect_fake_news(data["input"])
        return jsonify({
            "success": True, 
            "results": detailed_results,
            "formatted_results": "\n\n".join(formatted_results)
        })
    else:
        return jsonify({"success": False, "error": "Invalid request type."}), 400

def fetch_news(keywords, country=None, category=None):
    """Fetch news articles using the Newsdata.io API with advanced filtering."""
    params = {
        "apikey": NEWSDATA_API_KEY,
        "q": keywords,
        "language": "en",
    }
    
    if country:
        params["country"] = country
    
    if category:
        params["category"] = category
    
    response = requests.get(MEDIASTACK_BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        articles = [
            {
                "title": article.get("title", "No Title"),
                "description": article.get("description", "No Description"),
                "link": article.get("link", "#"),
            }
            for article in data.get("results", [])
        ]
        return jsonify({"success": True, "articles": articles})
    
    return jsonify({"success": False, "error": "Failed to fetch news."})

def generate_article(prompt):
    """Generate an article using the Gemini API."""
    url = f"{GEMINI_BASE_URL}?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Write a detailed article on the following topic: {prompt}. The article should be around 300-400 words long and cover key aspects of the subject."
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1000,
            "topP": 0.8,
            "topK": 10
        }
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            
            if 'candidates' in result and result['candidates']:
                content = result['candidates'][0]['content']['parts'][0]['text']
                return jsonify({"success": True, "response": content})
            else:
                return jsonify({"success": False, "error": "No content generated."})
        else:
            return jsonify({
                "success": False, 
                "error": f"API request failed with status {response.status_code}",
                "details": response.text
            })
    
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"An error occurred: {str(e)}"
        })

if __name__ == "__main__":
    app.run(debug=True)
