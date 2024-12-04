Here's an enhanced README file incorporating the fact-checking system for fake news detection.  

---

# FactCheckGen  

**FactCheckGen** is an advanced Flask-based application that integrates APIs to streamline news retrieval, article generation, and fake news detection. This tool is designed for journalists, content creators, and researchers who need real-time information, professional-grade articles, and reliable content verification.  

---

## Features  

1. **News Retrieval**  
   - Fetches up-to-date news articles based on user-provided keywords.  
   - Utilizes the *NewsData.io API* for real-time news aggregation.  
   - Displays titles and links to relevant articles (top 5 results).  

2. **AI-Powered Article Generation**  
   - Generates detailed, engaging articles using the *Gemini API*.  
   - Takes user-provided key points as input to produce professional-grade content.  

3. **Fake News Detection**  
   - Leverages machine learning models and APIs to detect the authenticity of news articles.  
   - Ensures the credibility of content, empowering users to avoid misinformation.  

4. **Seamless Integration**  
   - Combines APIs to deliver a robust platform for news and content creation.  
   - Offers an intuitive interface for multi-functional tasks.  

---

## Prerequisites  

Before running the application, ensure you have the following:  

1. **Python 3.x installed.**  
2. Flask, Requests, and relevant ML libraries installed. Install them using:  
   ```bash
   pip install flask requests scikit-learn pandas numpy
   ```  
3. API keys for:  
   - *NewsData.io*  
   - *Gemini API*  

---

## Installation  

1. Clone the repository:  
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```  

2. Replace the placeholder API keys in the `app.py` file:  
   - `NEWSDATA_API_KEY`  
   - `GEMINI_API_KEY`  

3. Set up the fake news detection system by including a pre-trained ML model (e.g., Logistic Regression or BERT).  

4. Run the application:  
   ```bash
   python app.py
   ```  

---

## Usage  

1. **News Retrieval**  
   - Enter a keyword to search for related news articles.  
   - The application fetches the top 5 articles and displays their titles and links.  

2. **Article Generation**  
   - Provide key points or a summary.  
   - The application generates a detailed article using AI.  

3. **Fake News Detection**  
   - Paste the text or URL of a news article.  
   - The application analyzes the content and labels it as **"Credible"** or **"Fake"** based on the pre-trained model.  

---

## Contribution  

Pull requests are welcome. For major changes, open an issue first to discuss your ideas. Ensure all contributions are well-documented.  


## Future Enhancements  

- Enhanced fake news detection with advanced NLP techniques.  
- Integration with additional APIs for broader news coverage.  
- Mobile-friendly interface for better accessibility.  





