# -*- coding: utf-8 -*-

import requests
import time
import json
import os
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

def extract_keywords(completion_executor, path="./keywords_per_stock"):
    preset_text = [{"role":"system","content":"어떤 종목에 대한 뉴스 기사별 핵심 키워드를 수집해서 최종적으로 해당 종목에 대한 키워드를 추출할거야.\n입력으로 종목의 이름과 키워드 목록이 주어지면 최대 5개의 키워드를 뽑고 그렇게 한 이유를 함께 설명해줘."},{"role":"user","content":"종목명: 삼성증권\n키워드 목록: [['ETF', '미국 전력 인프라 관련주', '공모주 펀드', '해외주식거래이벤트'], ['브로커리시 수수료수익', '대기업 오너 일가와 주식처분', 'WM 수수료 수익', '이동통신 서비스산업의 경제적 파급효과', '알테오젠 대표'], ['중개형ISA', '잔고 3조원 돌파', '108만 계좌 돌파', '점유율 1위'], ['KT', '영업이익', '무선 수익', 'IPTV'], ['산일전기', '일반 공모청약', '균등 배정 주식 수', '비례경쟁률'], ['중개형ISA', '계좌수108만'], ['해외주식 대체 입고 이벤트', '최대 400만원 지급'], ['한국거래소', 'OCIO 기관', '채권형', '주식형'], ['중개형ISA', '3조원 돌파', '108만 개'], ['SK텔레콤', '무선 매출', '영업이익', 'SK브로드밴드', 'AI 사업역량강화'], ['중개형 ISA', '국내주식', '해외주식ETF', '국내주식ETF'], ['중개형ISA', '3조원 돌파', '108만 개'], ['토스증권', 'WTS', 'NH투자증권', '하나로유통', '중개형ISA'], ['산일전기', '공모주 청약', '미래에셋증권'], ['MSCI', 'LS일렉트릭', 'SK아이이테크놀로지'], ['중개형개인종합자산관리계좌', 'ISA'], ['중개형ISA', '신규가입고객수', '유입자금', '국내주식46%', '해외주식ETF26%'], ['올림픽특수', '미디어', '전자', '디스플레이', '치킨', '주류', '편의점', '면세점', '제일기획', '이노션'], ['토스뱅크', '목돈굴리기', '국내 2-3개월 단기 채권', '미국 국채'], ['해외주식 거래 이벤트', '100달러 지급'], ['해외주식 이벤트', '타사 국내주식 대체 입고 이벤트'], ['해외주식 첫 거래 지원금'], ['해외주식 거래 이벤트'], ['해외주식 이벤트', '타사 국내주식 대체 입고 이벤트'], ['해외주식 이벤트', '타사 국내주식 대체 입고 이벤트'], ['엠팝', '홈화면 개편', '점유율 1위'], ['삼성증권 엠팝', '비대면 계좌개설', '투자정보 콘텐츠'], ['MTS', '엠팝', '홈 화면 개편'], ['엠팝', '점유율 1위', '홈 화면 개편'], ['금융투자소득세', '금투세', '전산작업'], ['mPOP', 'S.Lounge', '로보굴링'], ['엠팝', '홈 화면 개편'], ['엠팝', 'S.Lounge', '로보굴링'], ['타사 해외주식 대체 입고 이벤트', '리워드 지급']]\n"},{"role":"assistant","content":"삼성증권에 대한 키워드는 다음과 같이 추출할 수 있습니다.  \n\n1. ETF : 삼성증권은 다양한 ETF 상품을 제공하고 있으며, 미국 전력 인프라 관련주 등 다양한 테마의 ETF 상품을 출시하였습니다. \n2. 중개형ISA : 삼성증권의 중개형ISA는 잔고 3조원을 돌파하며 108만 계좌를 돌파하였으며, 점유율 1위를 차지하고 있습니다. 이는 국내주식 뿐만 아니라 해외주식ETF, 국내주식ETF도 거래가 가능하기 때문입니다.\n3. 해외주식 이벤트 : 삼성증권은 해외주식 첫 거래 지원금, 100달러 지급 등 다양한 해외주식 이벤트를 진행하여 고객들의 관심을 끌고 있습니다.\n4. 엠팝 : 삼성증권의 모바일 앱인 엠팝은 홈 화면 개편을 통해 사용자들의 편의성을 높이고, 점유율 1위를 차지하고 있습니다. \n\n위와 같은 키워드로 삼성증권을 설명할 수 있으며, 이를 바탕으로 삼성증권에 대한 마케팅 문구를 작성하거나, 삼성증권과 관련된 뉴스 기사를 검색할 때 유용하게 활용할 수 있습니다."}]
    for file_name in os.listdir(path):
        stock = file_name.split("_")[0]
        with open(os.path.join(path, file_name), "r", encoding="utf-8") as f:
            news_list = json.load(f)
            content = f"종목명: {stock}\n키워드 목록: ["
            for news in news_list:
                content += str(news['keywords']) + ', '
            content = content[:-2] + ']'
            print(content)
            exit()
    # for news in news_list:
    #     content = news['summary']
    #     user_query = [{"role":"user", "content": f"Focus: {focus}\n{content}"}]
    #     request_data = {
    #         'messages': preset_text + user_query,
    #         'topP': 0.8,
    #         'topK': 0,
    #         'maxTokens': 502,
    #         'temperature': 0.5,
    #         'repeatPenalty': 5.0,
    #         'stopBefore': [],
    #         'includeAiFilters': True,
    #         'seed': 0
    #     }

    #     result = completion_executor.execute(request_data)
    #     print(content)
    #     raw_keyword_list = result['message']['content'][1:-1].split(',')
    #     keywords = [
    #         keyword.strip()
    #         for keyword in raw_keyword_list
    #         if keyword.strip() not in [focus, ""]
    #     ]
    #     news['keywords'] = keywords
    #     print(keywords)
        
    # return news_list      


if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYw3uGNnTgIt0AjzNuqcIgFp5ylO92dJG1LY2R2/SQS8a',
        api_key_primary_val='YoSx0SuFB8posSy0xxdLUk6yZCMdvSYzWZ6XY9EH',
        request_id='f7307d34-a931-4eb3-b022-f8c4077bf38a'
    )
    
    extracted_keywords = extract_keywords(completion_executor)
    
    # with open(f"keywords_per_stock/{args.stock}_keywords.json", "w", encoding="utf-8") as f:
    #     json.dump(extracted_keywords, f, ensure_ascii=False, indent=4)    