import json

def extract_keywords():
    with open("keywords_per_stocks.json", "r", encoding='utf-8') as json_data:
        companies = json.load(json_data)
        for company, details in companies.items():
            keywords = ', '.join(details["keywords"])
            print(f"{company}: {keywords}")
            
if __name__ == "__main__":
    extract_keywords()
