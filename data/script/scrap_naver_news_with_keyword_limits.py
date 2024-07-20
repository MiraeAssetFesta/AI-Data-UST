import requests
import json
import time
import warnings
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from argparse import ArgumentParser
from env import client_id, client_secret

warnings.filterwarnings('ignore')

def scrap_naver_news(keyword, limits):
    base_url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    articles = []
    start = 1
    # limit_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    params = {
        "query": keyword,
        "sort": "date",
        "start": start,
        "display": 100
    }
    response = requests.get(base_url, headers=headers, params=params, verify=False)
    data = response.json()

    cnt = 0
    cnt_per_date = {}
    while cnt < limits:
        try:
            for item in data['items']:
                pub_date = datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S +0900').strftime('%Y-%m-%d')
                cnt_per_date.setdefault(pub_date, 0)
                if cnt_per_date[pub_date] == 20: 
                    break
                cnt_per_date[pub_date] += 1
                # description = item['description']
                link = item['link']
                if article_content := fetch_article_content(link):
                    title = item['title']
                    articles.append({"date": pub_date, "title": title, "content": article_content})
                    cnt += 1

            start += 100
            params = {
                "query": keyword,
                "sort": "date",
                "start": start,
                "display": 100
            }
            response = requests.get(base_url, headers=headers, params=params, verify=False)
            data = response.json()
        except:
            break
                
                
    return articles


def fetch_article_content(url):
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return "\n".join([p.get_text() for p in paragraphs])
    except Exception as e:
        print(f"Error fetching article content from {url}: {e}")
        return None


def main():
    parser = ArgumentParser()
    parser.add_argument("--keyword", type=str, help="Keyword to search news articles", required=True)
    parser.add_argument("--limits", type=int, help="Number of limits to search news articles", default=3)
    args = parser.parse_args()
    
    keyword = args.keyword
    limits = args.limits
    articles = scrap_naver_news(keyword, limits)
    
    with open(f"../{keyword}_news.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)    
    
if __name__ == "__main__":
    main()
