# -*- coding: utf-8 -*-

import requests
import json
import time
from argparse import ArgumentParser
from env import api_key, api_key_primary_val


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
    preset_text = [{"role":"system","content":"keyword와 content가 주어지면 content가 keyword와 관련있는지 판단할거야.\n먼저, keyword가 무엇인지 네이버에서 검색했을 때 나오는 정보로 한 줄로 요약해.\n다음으로, keyword가 content에서 '직접적인' 연관이 있는지 문단별로 판단하고 설명을 덧붙여.\n마지막으로, 최종적으로 content가 keyword와 관련있는지 True 또는 False로 출력해."},
                    {"role":"user","content":"keyword: 삼성증권\r\ncontent: - 금융권이 연준 금리인하, 미국 대선 등의 변화가 예견되는 시장에 대응하기 위해 주식 비중, 미국·인도 주식 시장, 채권·금 등을 성공 투자 키 포인트로 제시함\\n- SC제일은행은 자산관리(WM) 고객을 위한 ‘2024년 하반기 글로벌 금융시장 전망 및 투자전략 보고서’를 발표함\\n- 하반기에는 연준의 금리인하, 미국 대선 등 정책 측면의 전환점이 가까워지고 있어 변화의 물결을 거스르지 않고 새로운 환경에 빠르게 적응하며 더 큰 투자의 기회를 찾을 것을 강조함\\n- 2분기부터 시작된 주요국 중앙은행들의 금리인하 기조는 하반기에도 이어질 것으로 전망함\\n- 미 연준 역시 임대료 하락 및 고용시장 둔화 등에 따른 물가 압력 완화를 바탕으로 하반기 중 금리인하를 단행할 것으로 예측함\\n- 정책의 초점은 물가 억제에서 성장률 지원으로 이동할 것이라 말함\\n- 미국 대선이 각종 뉴스의 헤드라인을 장식하겠지만 투자자들은 거시경제 및 시장의 펀더멘털 요인에 관심을 기울이는 것이 더욱 중요하다고 분석함\\n- 제조업 경기가 하반기 글로벌 경기를 주도할 것으로 예상하는 가운데 금리 인하가 더해지면서 위험자산의 강세가 지속될 것으로 봄\\n- 지난 상반기 증시의 상승 랠리를 주도한 성장주는 하반기에도 호조세가 지속될 것으로 전망함\\n- KB금융은 하반기에는 채권투자에 큰 관심을 가질 필요가 있다고 제언함\\n- 연준의 통화 완화 전환기대가 시장금리의 하향 안정화로 이어질 것이라는 전망 때문임\\n- 단기채나 중기채 위주로 투자하는 전략이 적합함\\n- 삼성증권 디지털자산관리본부가 지난달 11∼14일 삼성증권 예탁 자산 5억 원 이상의 S.라운지(Lounge) 고객을 대상으로 설문조사한 결과를 알려주고 있음\r\n\r\n"},
                    {"role":"assistant","content":"삼성증권 : \n주식 거래 서비스를 제공하는 대한민국의 증권사  \n\ncontent와의 관련성 :\n해당 보고서에서는 금융권의 2024년 하반기 글로벌 금융시장 전망과 투자전략에 대해 다루고 있으며, 이 중 삼성증권에서도 자사 고객들을 대상으로 설문조사를 진행한 바 있습니다. 따라서 해당 보고서 내 일부 내용이 삼성증권과 관련이 있다고 볼 수 있습니다.\n\n최종 판단 : \nTrue"},
                    {"role":"user","content":"keyword: LG화학\ncontent: - 미 대선 관련주의 등락이 반복되면서 투자자들의 우려가 커짐\\n- 도널드 트럼프 미국 공화당 대선 후보의 발언 이후 반도체주를 향한 투심이 얼어 붙음\\n- 2차전지 관련주 전망에 이목이 집중되고 있음\\n- 트럼프의 발언 이후 반도체 관련주가 급락함\\n- 올해 상반기 상승 랠리가 지속된 미국 증시가 흔들리면서 국내 반도체주도 주가 조정을 겪고 있음\\n- 금리 인하 기대감으로 중소형주로 순환매가 진행된 것과 함께 정책 리스크가 불거졌지만, 기업들의 견조한 실적을 바탕으로 주가 상승 여력은 충분함\\n- 2차전지 관련주의 불확실성은 더욱 커진 분위기임\\n- 트럼프 후보가 당선될 경우 세액공제와 보조금이 줄면서 국내 배터리 기업도 업황 부진을 겪을 가능성이 높음\\n- 트럼프의 피습 사건 이후 급락한 2차전지·양극재 관련주는 10일 저가매수세 유입으로 일부 상승 흐름을 보이고 있음\\n- 증권가에서는 전기차 캐즘 현상에 따른 업황 부진에 이어 미 대선 리스크가 가중되면서 관련주가 조정기를 한번 더 거칠 것이라는 시각이 나옴\\n- 바이든 대통령에 대해 미국 민주당 지지층들의 후보 사퇴 요구가 제기됨\\n- 후보가 교체될 경우 2차전지주가 상승 여력을 확보할 수 있다는 의견도 있음"},
                    {"role":"assistant","content":"LG화학 : \n대한민국의 화학 기업이며, 2차전지 관련 사업을 영위하고 있음\n\ncontent와의 관련성 :  \n미 대선 관련주의 등락이 반복되면서 2차전지 관련주인 LG화학 또한 영향을 받을 수 있음을 시사하고 있습니다. 특히, 트럼프 후보가 당선될 경우 세액공제와 보조금이 줄어들며 국내 배터리 기업 의 업황 부진이 예상된다는 의견이 있습니다.\n\n최종 판단 : \nTrue"},
                    # {"role":"user","content":"keyword: 삼성증권\ncontent: - 삼성증권이 6월말 기준으로 중개형ISA 잔고 3조원을 돌파했다고 밝힘\\n- 중개형ISA 계좌수도 108만개를 넘어섰다고 밝힘\\n- 삼성증권의 중개형ISA 가입고객을 분석한 결과, 올 상반기동안 중개형ISA 신규가입고객수와 유입자금이 지난해 전체 가입자수와 유입자금을 넘어섰을 정도로 관심이 높아졌음\\n- 삼성증권은 중개형ISA 업계전체 점유율이 각각 21%(잔고)와 24%(계좌)를 기록할 만큼 중개형 ISA의 명가로 평가받고 있음\\n- 삼성증권 중개형ISA 가입 고객들의 자산을 분석한 결과, 국내주식 46% / 해외주식ETF 26% / 국내주식ETF 6% 등으로 투자자금의 79%를 주식형 자산에 투자하고 있는 것으로 나타남\\n- 중개형ISA 계좌를 통한 절세혜택을 활용하려는 스마트한 투자자들이 많은 것으로 확인됨"},
                    # {"role":"assistant","content":"삼성증권 : \n주식 거래 서비스를 제공하는 대한민국의 증권사\n\ncontent와의 관련성 : \n본 글에서는 삼성증권이 중개형ISA 잔고 3조원을 돌파했다는 소식을 전하고 있으며, 이를 통해 삼성증권의 성과를 알리고 있습니다.\n\n최종 판단 : \nTrue"}
                ]    
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
        api_key=api_key,
        api_key_primary_val=api_key_primary_val,
        request_id='16943d15-eb47-45fb-b9ae-a38200cb9ce7'
    )
    
    news_list = json.load(open(f"../{args.stock}_summarized_news.json", "r", encoding="utf-8"))
    passed_news = filter_news(news_list, args.stock, completion_executor)
    
    with open(f"../{args.stock}_passed_news.json", "w", encoding="utf-8") as f:
        json.dump(passed_news, f, ensure_ascii=False, indent=4)    
    