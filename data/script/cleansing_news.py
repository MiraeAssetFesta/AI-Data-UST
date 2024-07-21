import json
import re
import warnings
from argparse import ArgumentParser

warnings.filterwarnings('ignore')

def load_news_articles(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    return articles

def clean_articles(keyword, articles):
    cleaned_articles = []
    for article in articles:
        title = article['title']
        content = article['content']
        # Remove special characters
        content = content.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        # Remove unnecessary whitespaces
        content = ' '.join(content.split())
        # Remove Html tags
        title = re.sub(r'<.*?>', '', title)
        content = re.sub(r'<.*?>', '', content)
        # Remove Html word entities
        title = re.sub(r'&.*?;', '', title)
        content = re.sub(r'&.*?;', '', content)
        # 키워드가 포함되지 않았다면 제외, 증권 관련이면 보통 키워드 포함
        if keyword not in content and keyword.replace(' ', '') not in content:
            continue
        # # 한국어가 깨졌다면 제외
        # if not re.search(r'[^ᄀ-힣\s@]', content):
        #     continue        
        # 4000문자가 넘는건 대부분 광고기사이므로 제외
        if len(content) > 4000:
            continue
        # 특정 문자열을 포함하는 기사 제외
        if '언론사 구독 해지되었습니다.' in content \
            or '열린보도원칙 당 매체는' in content \
            or '글로벌에픽' in content \
            or '아시아투데이' in content \
            or '전체기사 산업·IT·과학 경제일반' in content :
            continue
            
        date = article['date']
        cleaned_articles.append({'date': date, 'title': title, 'content': content})
    return cleaned_articles

def save_articles(articles, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

def main():
    parser = ArgumentParser()
    parser.add_argument("--keyword", type=str, help="Keyword to search news articles", required=True)
    args = parser.parse_args()
    keyword = args.keyword
    articles = load_news_articles(f"../{keyword}_news.json")
    cleaned_articles = clean_articles(keyword, articles)
    save_articles(cleaned_articles, f"../{keyword}_cleaned_news.json")

if __name__ == "__main__":
    main()