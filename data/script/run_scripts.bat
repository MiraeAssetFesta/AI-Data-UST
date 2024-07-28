chcp 65001

REM SPDR S&P 500 ETF에 대해 스크립트 실행
python 1.scrap_naver_news_with_keyword_limits.py --stock "SPDR S&P 500 ETF"
python 2.cleansing_news.py --stock "SPDR S&P 500 ETF"
python 3.summary_news.py --stock "SPDR S&P 500 ETF"  
python 4.judge_news.py --stock "SPDR S&P 500 ETF"      
python 5.extract_keywords_from_news.py --stock "SPDR S&P 500 ETF" 

REM 애플에 대해 스크립트 실행
python 1.scrap_naver_news_with_keyword_limits.py --stock "애플"
python 2.cleansing_news.py --stock "애플"
python 3.summary_news.py --stock "애플"  
python 4.judge_news.py --stock "애플"      
python 5.extract_keywords_from_news.py --stock "애플"  

REM 아마존에 대해 스크립트 실행
python 1.scrap_naver_news_with_keyword_limits.py --stock "아마존"
python 2.cleansing_news.py --stock "아마존"
python 3.summary_news.py --stock "아마존"  
python 4.judge_news.py --stock "아마존"      
python 5.extract_keywords_from_news.py --stock "아마존"  

REM 최종 결과물 생성
python 6.extract_keywords_from_stock.py     

chcp 949

pause
