# -*- coding: utf-8 -*-

import requests
import time
import json
from argparse import ArgumentParser


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        result = "Error"
        while result == "Error":
            with requests.post(self._host + '/testapp/v1/chat-completions/HCX-DASH-001',
                            headers=headers, json=completion_request, stream=True) as r:
                for line in r.iter_lines():
                    if line and "result" in line.decode("utf-8"):
                        result = line.decode("utf-8") 
            if result == "Error":
                print("Error occurred. Retrying...")
                time.sleep(30)
        
        return json.loads(result[5:])
    

def extract_keywords(news_list, stock, completion_executor):
    preset_text = [{"role":"system","content":"뉴스기사로부터 최대 10개의 핵심 키워드를 추출할거야. Focus가 주어지면 해당 키워드와 관련한 키워드만 뽑고 관련없는 키워드는 제외해.\n출력 양식: [키워드1, 키워드2, ...]"},{"role":"user","content":"Focus: 삼성증권\r\n- 투자상품 시장에서 단기자금 운용 목적의 ETF가 나와 주목됨\\n- 미국 전력 인프라 관련주에 투자하는 ETF도 출시됨\\n- 익일 출금이 가능한 공모주 펀드도 출시됨\\n- 해외주식 투자와 관련한 이벤트가 다수 나옴\\n- 김현빈 NH아문디자산운용 ETF투자본부장은 주식시장에서 편리한 매수, 매도를 통해 국내 머니마켓에 투자할 수 있다는 장점이 있다고 함\\n- 신한자산운용은 ‘SOL 미국 AI 전력인프라’ ETF를 출시함\\n- 다올자산운용은 업계 최초로 다음 날 출금이 가능한 채권혼합형 상품 ‘다올내일출금공모주펀드’를 출시함\\n- 채권혼합형 상품으로는 업계 최초로 ETF보다 빠른 익영업일(T+1)일 출금이 가능해짐\\n- 공모주는 펀드 순자산 총액의 5% 이하로 투자함\\n- 밸류에이션 분석을 통해 보수적으로 수요예측에 참여하고 미확약으로 청약을 진행함\\n- 공모주펀드 투자의 적기임\\n- 공모주 투자를 통한 추가 수익을 기대할 수 있고 익일 출금으로 환금성까지 갖춘 매력적인 상품임\\n- 삼성증권에서 해외주식 거래가 없던 고객을 대상으로 최대 100달러를 지급하는 이벤트를 진행함"},{"role":"assistant","content":"[삼성증권, ETF, 미국 전력 인프라 관련주, 공모주 펀드,  해외주식거래이벤트]"},{"role":"user","content":"Focus: 삼성증권\r\n- 삼성증권에 대한 내용을 다루고 있는 문서를 공유함\\n- 삼성증권의 1분기 브로커리지 수수료수익은 1624억원으로 전년 동기 1230억원 대비 32.0% 늘었음\\n- 대기업 오너 일가의 주식 처분 현황을 공유함\\n- 삼성증권의 1분기 브로커리지와 WM 수수료 수익 추이를 보여주고 있음\\n- 이동통신 서비스산업의 경제적 파급효과에 대해 이야기하고 있음\\n- 박순재 알테오젠 대표가 주식가치가 39% 상승하여 10위권에 첫 진입함\\n- 2024년 500대 기업과 중견기업 리스트를 보여주고 있음"},{"role":"assistant","content":"[삼성증권, 브로커리지 수수료수익, 대기업 오너 일가와 주식 처분, WM 수수료 수익 ]"}]
    for news in news_list:
        content = news['summary']
        user_query = [{"role":"user", "content": f"Focus: {stock}\n{content}"}]
        request_data = {
            'messages': preset_text + user_query,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 502,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        result = completion_executor.execute(request_data)
        print(content)
        raw_keyword_list = result['message']['content'][1:-1].split(',')
        keywords = [
            keyword.strip()
            for keyword in raw_keyword_list
            if keyword.strip() not in [stock, ""]
        ]
        news['keywords'] = keywords
        print(keywords)
        
    return news_list        


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--stock", type=str, required=True)
    args = parser.parse_args()
    
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYw3uGNnTgIt0AjzNuqcIgFp5ylO92dJG1LY2R2/SQS8a',
        api_key_primary_val='YoSx0SuFB8posSy0xxdLUk6yZCMdvSYzWZ6XY9EH',
        request_id='9fe15107-403c-43d2-b983-93eb254cc4e3'
    )
    
    news_list = json.load(open(f"../{args.stock}_passed_news.json", "r", encoding="utf-8"))
    extracted_keywords = extract_keywords(news_list, args.stock, completion_executor)
    
    with open(f"../keywords_per_stock/{args.stock}_keywords.json", "w", encoding="utf-8") as f:
        json.dump(extracted_keywords, f, ensure_ascii=False, indent=4)    

