# -*- coding: utf-8 -*-

import requests
import json
import time
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

    
def filter_news(news_list, stock, completion_executor):
    preset_text = [{"role":"system","content":"keyword와 content가 주어지면 content가 keyword와 관련있는지 판단할거야.\n먼저, keyword가 무엇인지 네이버에서 검색했을 때 나오는 정보로 한 줄로 요약해.\n다음으로, keyword가 content에서 '직접적인' 연관이 있는지 문단별로 판단하고 설명을 덧붙여.\n마지막으로, 최종적으로 content가 keyword와 관련있는지 True 또는 False로 출력해."},{"role":"user","content":"keyword: 삼성증권\r\ncontent: - 금융권이 연준 금리인하, 미국 대선 등의 변화가 예견되는 시장에 대응하기 위해 주식 비중, 미국·인도 주식 시장, 채권·금 등을 성공 투자 키 포인트로 제시함\\n- SC제일은행은 자산관리(WM) 고객을 위한 ‘2024년 하반기 글로벌 금융시장 전망 및 투자전략 보고서’를 발표함\\n- 하반기에는 연준의 금리인하, 미국 대선 등 정책 측면의 전환점이 가까워지고 있어 변화의 물결을 거스르지 않고 새로운 환경에 빠르게 적응하며 더 큰 투자의 기회를 찾을 것을 강조함\\n- 2분기부터 시작된 주요국 중앙은행들의 금리인하 기조는 하반기에도 이어질 것으로 전망함\\n- 미 연준 역시 임대료 하락 및 고용시장 둔화 등에 따른 물가 압력 완화를 바탕으로 하반기 중 금리인하를 단행할 것으로 예측함\\n- 정책의 초점은 물가 억제에서 성장률 지원으로 이동할 것이라 말함\\n- 미국 대선이 각종 뉴스의 헤드라인을 장식하겠지만 투자자들은 거시경제 및 시장의 펀더멘털 요인에 관심을 기울이는 것이 더욱 중요하다고 분석함\\n- 제조업 경기가 하반기 글로벌 경기를 주도할 것으로 예상하는 가운데 금리 인하가 더해지면서 위험자산의 강세가 지속될 것으로 봄\\n- 지난 상반기 증시의 상승 랠리를 주도한 성장주는 하반기에도 호조세가 지속될 것으로 전망함\\n- KB금융은 하반기에는 채권투자에 큰 관심을 가질 필요가 있다고 제언함\\n- 연준의 통화 완화 전환기대가 시장금리의 하향 안정화로 이어질 것이라는 전망 때문임\\n- 단기채나 중기채 위주로 투자하는 전략이 적합함\\n- 삼성증권 디지털자산관리본부가 지난달 11∼14일 삼성증권 예탁 자산 5억 원 이상의 S.라운지(Lounge) 고객을 대상으로 설문조사한 결과를 알려주고 있음\r\n\r\n"},{"role":"assistant","content":"삼성증권 : \n주식 거래 서비스를 제공하는 대한민국의 증권사  \n\ncontent와의 관련성 :\n해당 보고서에서는 금융권의 2024년 하반기 글로벌 금융시장 전망과 투자전략에 대해 다루고 있으며, 이 중 삼성증권에서도 자사 고객들을 대상으로 설문조사를 진행한 바 있습니다. 따라서 해당 보고서 내 일부 내용이 삼성증권과 관련이 있다고 볼 수 있습니다.\n\n최종 판단 : \nTrue"},{"role":"user","content":"keyword: 삼성증권\ncontent: - 토스증권은 모기업 토스의 영향력 아래 사뿐히 발을 들였지만, 원년(2021년) 쓴맛을 봄\\n- 김승연 대표가 부임한 뒤 혁신의 혁신을 거듭한 토스증권은 지난해 영업적자를 눈부시게 줄임\\n- 올해 영업흑자를 기록할 수 있을 것으로 기대되고 있음\\n- 금융과는 관련이 없는 기업들에서 경영 능력을 입증함\\n- 토스증권 대표로 부임한 김승연 대표는 고객에게 더 나은 서비스를 제공하겠다는 목표를 가지고 리테일 브로커리지(위탁매매)에 모든 역량을 집중함\\n- 그의 인사이트는 통했고, 토스증권은 삼성증권·미래에셋·키움증권 등 기존 증권사들과의 해외주식 수수료 싸움에서 밀리지 않고 있음\\n- 토스증권의 김 대표는 웹트레이딩시스템(WTS)과 해외 채권투자, 파생상품 등을 통해 금융시장 파이를 차지하겠다는 포부임\\n- DSS(Payment Card Industry Data Security Standard)’ 인증을 취득함"},{"role":"assistant","content":"삼성증권 : \n주식 거래 서비스를 제공하는 대한민국의 증권사\n\ncontent와의 관련성 :  \n토스증권대표 김승연씨가 삼성증권 출신인 점 이외에는 삼성증권과 관련된 정보를 찾을 수 없습니다.\n\n최종 판단 : \nFalse"},{"role":"user","content":"keyword: 삼성증권\ncontent: - 삼성증권이 6월말 기준으로 중개형ISA 잔고 3조원을 돌파했다고 밝힘\\n- 중개형ISA 계좌수도 108만개를 넘어섰다고 밝힘\\n- 삼성증권의 중개형ISA 가입고객을 분석한 결과, 올 상반기동안 중개형ISA 신규가입고객수와 유입자금이 지난해 전체 가입자수와 유입자금을 넘어섰을 정도로 관심이 높아졌음\\n- 삼성증권은 중개형ISA 업계전체 점유율이 각각 21%(잔고)와 24%(계좌)를 기록할 만큼 중개형 ISA의 명가로 평가받고 있음\\n- 삼성증권 중개형ISA 가입 고객들의 자산을 분석한 결과, 국내주식 46% / 해외주식ETF 26% / 국내주식ETF 6% 등으로 투자자금의 79%를 주식형 자산에 투자하고 있는 것으로 나타남\\n- 중개형ISA 계좌를 통한 절세혜택을 활용하려는 스마트한 투자자들이 많은 것으로 확인됨"},{"role":"assistant","content":"삼성증권 : \n주식 거래 서비스를 제공하는 대한민국의 증권사\n\ncontent와의 관련성 : \n본 글에서는 삼성증권이 중개형ISA 잔고 3조원을 돌파했다는 소식을 전하고 있으며, 이를 통해 삼성증권의 성과를 알리고 있습니다.\n\n최종 판단 : \nTrue"}]    
    passed_news = []
    for news in news_list:
        content = news['summary']
        user_query = [{"role":"user", "content": f"keyword: {stock}\ncontent: {content}"}]
        request_data = {
            'messages': preset_text+user_query,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 502,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': ['keyword'],
            'includeAiFilters': True,
            'seed': 0
        }

        result = completion_executor.execute(request_data)
        print(content)
        print(result['message']['content'])
        result_tf = result['message']['content'].split("\n")[-1].strip() == "True"
        if result_tf:
            passed_news.append(news)
    return passed_news        


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--stock", type=str, required=True)
    args = parser.parse_args()
    
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYw3uGNnTgIt0AjzNuqcIgFp5ylO92dJG1LY2R2/SQS8a',
        api_key_primary_val='YoSx0SuFB8posSy0xxdLUk6yZCMdvSYzWZ6XY9EH',
        request_id='16943d15-eb47-45fb-b9ae-a38200cb9ce7'
    )
    
    news_list = json.load(open(f"../{args.stock}_summarized_news.json", "r", encoding="utf-8"))
    passed_news = filter_news(news_list, args.stock, completion_executor)
    
    with open(f"../{args.stock}_passed_news.json", "w", encoding="utf-8") as f:
        json.dump(passed_news, f, ensure_ascii=False, indent=4)    
    