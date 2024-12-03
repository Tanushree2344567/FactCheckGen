import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# NewsData.io API Configuration
NEWSDATA_API_KEY =   # Replace with your actual NewsData.io API key
NEWSDATA_BASE_URL = "https://newsdata.io/api/1/news"

def fetch_current_news(keywords=None, country=None, category=None):
    """
    Fetch current news articles using NewsData.io API
    
    Parameters:
    - keywords: Optional search keywords
    - country: Optional country code (e.g., 'us', 'in')
    - category: Optional news category (e.g., 'technology', 'business')
    """
    params = {
        "apikey": NEWSDATA_API_KEY,
        "language": "en"  # English language news
    }
    
    # Add optional parameters if provided
    if keywords:
        params["qInTitle"] = keywords
    if country:
        params["country"] = country
    if category:
        params["category"] = category
    
    try:
        response = requests.get(NEWSDATA_BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        
        data = response.json()
        
        if data.get('results'):
            # Process and return news articles
            news_articles = []
            for article in data['results']:
                news_articles.append({
                    "title": article.get('title', 'No Title'),
                    "description": article.get('description', 'No Description'),
                    "link": article.get('link', ''),
                    "published_at": article.get('pubDate', 'Unknown Date'),
                    "source": article.get('source_id', 'Unknown Source')
                })
            
            return news_articles
        else:
            return []
    
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return []

@app.route("/")
def index():
    return render_template("inde.html")

@app.route("/fetch_news", methods=["POST"])
def fetch_news():
    try:
        # Get parameters from the request
        data = request.json
        keywords = data.get('keywords')
        country = data.get('country')
        category = data.get('category')
        
        # Fetch news based on parameters
        news_articles = fetch_current_news(
            keywords=keywords, 
            country=country, 
            category=category
        )
        
        if news_articles:
            return jsonify({
                "status": "success",
                "articles": news_articles
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No news articles found"
            }), 404
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
