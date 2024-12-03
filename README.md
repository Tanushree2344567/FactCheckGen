# FactCheckGen
This project uses a combination of APIs and tools to create a system that generates articles, news, and detects fake news.

This project is a Flask-based application that integrates the NewsData.io API and the Gemini API to streamline news retrieval and article generation. It allows users to search for real-time news articles based on keywords and generate detailed, AI-powered articles from structured key points. By combining these functionalities, the application serves as a powerful tool for content creation, news aggregation, and information retrieval, making it ideal for journalists, content creators, and researchers.

 Features  :

 1. News Retrieval:
- Fetches up-to-date news articles based on user-provided keywords.  
- Utilizes the *NewsData.io API* for real-time news aggregation.  
- Displays titles and links to relevant articles, limited to the top 5 results for quick access.  

2. AI-Powered Article Generation:
- Generates detailed, engaging articles using the *Gemini API*.  
- Takes user-provided key points as input to produce professional-grade content.  

3. Seamless Integration:
- Combines APIs to deliver a robust platform for news and content creation.  
- Designed for journalists, content creators, and researchers who need fast, reliable, and high-quality information.  

---

Prerequisites  

Before running the application, ensure you have the following:  
1. Python 3.x installed.  
2. Flask and Requests libraries installed. Install them using:  
   bash
   pip install flask requests
   
3. API keys for:  
   - *NewsData.io*  
   - *Gemini API*  

---

> Installation  

1. Clone the repository:  
   bash
   git clone https://github.com/your-username/content-generation-news-retrieval.git
   cd content-generation-news-retrieval
     

2. Replace the placeholder API keys in the app.py file:  
   - NEWSDATA_API_KEY  
   - GEMINI_API_KEY  

3. Run the application:  
   bash
   python app.py
     

4. Access the application in your browser at:  
   
   http://127.0.0.1:5000/

   
### Usage  

1. News Retrieval
   - Enter a keyword to search for related news articles.  
   - The application will fetch the top 5 articles and display their titles and links.  

2. Article Generation  
   - Provide key points or a summary.  
   - The application will generate a detailed article using AI.  


# Folder Structure  


content-generation-news-retrieval/
│
├── templates/
│   └── index.html          # Frontend HTML template
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
  





