import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# NewsData.io API Configuration
NEWSDATA_API_KEY = "pub_611749570cd796321c0b0de8c8c0f4c762b92"  # Replace with your actual NewsData.io API key
NEWSDATA_BASE_URL = "https://newsdata.io/api/1/news"

def fetch_current_news(keywords=None, country=None, category=None, language='en', page=None):
    """
    Fetch current news articles using NewsData.io API with advanced filtering
    
    Parameters:
    - keywords: Optional search keywords
    - country: Optional country code (e.g., 'us', 'in')
    - category: Optional news category 
    - language: Language of news (default: English)
    - page: Pagination token for fetching next set of results
    """
    params = {
        "apikey": NEWSDATA_API_KEY,
        "language": language
    }
    
    # Add optional parameters if provided
    if keywords:
        params["qInTitle"] = keywords
    if country:
        params["country"] = country
    if category:
        params["category"] = category
    if page:
        params["page"] = page
    
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
                    "source": article.get('source_id', 'Unknown Source'),
                    "country": article.get('country', ['Unknown'])[0]
                })
            
            return {
                "articles": news_articles,
                "next_page": data.get('nextPage')
            }
        else:
            return {"articles": [], "next_page": None}
    
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return {"articles": [], "next_page": None}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/handle_request", methods=["POST"])
def handle_request():
    try:
        # Get user input and type
        data = request.json
        user_input = data.get('input')
        request_type = data.get('type')  # "news" or "article"
        
        # Additional news filtering parameters
        country = data.get('country', '')
        category = data.get('category', '')
        language = data.get('language', 'en')
        page = data.get('page')

        if request_type == "news":
            # Fetch current news with advanced filtering
            news_result = fetch_current_news(
                keywords=user_input,
                country=country,
                category=category,
                language=language,
                page=page
            )
            
            if news_result['articles']:
                return jsonify({
                    "type": "news", 
                    "response": news_result['articles'],
                    "next_page": news_result['next_page']
                })
            else:
                return jsonify({
                    "type": "news",
                    "error": "No news articles found",
                    "response": []
                }), 404

        else:
            return jsonify({"error": "Invalid request type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)