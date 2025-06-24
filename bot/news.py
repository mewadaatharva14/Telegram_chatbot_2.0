
from bs4 import BeautifulSoup
import requests

def get_latest_news(max_articles=5):
    url = "https://www.hindustantimes.com/topic/ahmedabad/news"
    headers = {'User-Agent': "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    articles = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headings = soup.find_all('h3')

        for h in headings:
            if "hdg3" in h.get("class", []):
                title = h.text.strip()
                if title not in articles:
                    articles.append(title)
                if len(articles) >= max_articles:
                    break
    else:
        articles.append(f"Failed to fetch news: {response.status_code}")

    return articles
