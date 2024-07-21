# -*- coding: utf-8 -*-

import base64
import json
import http.client
import time
from argparse import ArgumentParser
from script.env import api_key, api_key_primary_val


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/api-tools/summarization/v2/dfb1f2d627db448b87645f73b13ad312', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        return res['result']['text'] if res['status']['code'] == '20000' else 'Error'


def summarize_news(stock, completion_executor):
    with open(f"../{stock}_cleaned_news.json", 'r', encoding='utf-8') as f:
        news_list = json.load(f)
        for news in news_list:
            request_data = json.loads('{"texts" : [ "' + \
                f"다음 문서는 {stock}에 대한 내용을 다루고 있습니다. > " + news['content'].replace('\"', '\\\"') + '" ],' + \
""" "segMinSize" : 300,
    "includeAiFilters" : true,
    "autoSentenceSplitter" : true,
    "segCount" : -1,
    "segMaxSize" : 1000
}""", strict=False)
            summarized = "Error"
            while summarized == "Error":
                summarized = completion_executor.execute(request_data)
                if summarized == "Error":
                    print("Error occurred. Retrying...")
                    time.sleep(30)
            news['summary'] = summarized
    return news_list 


def save_summary_news(stock, news_list):
    with open(f'../{stock}_summarized_news.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--stock', type=str, required=True)
    args = parser.parse_args()
    
    completion_executor = CompletionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key = api_key,
        api_key_primary_val = api_key_primary_val,
        request_id='06240e24-40a9-4127-85b3-7cf0e96ab8e4'
    )
    result = summarize_news(args.stock, completion_executor)
    save_summary_news(args.stock, result)
