import feedparser
import pandas as pd
import datetime


# rss url을 전달 받아 파싱해준다
def parseRSS(rss_url):
    return feedparser.parse(rss_url)

# 파싱된 rss 데이터 가공
# index / 구분 (구글) / 검색어 / 내용 / 검색 횟수 / 링크
def getTrendsInfo(rss_url, rss_key) :
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    keywords = []
    traffic = []
    itemtitle = []
    itemlink = []

    feed = parseRSS(rss_url)
    for trends_item in feed['entries']:
        keywords.append(trends_item['title'])
        traffic.append(trends_item['ht_approx_traffic'])
        itemtitle.append(trends_item['ht_news_item_title'])
        itemlink.append(trends_item['ht_news_item_url'])

    trend_keywords = pd.Series(keywords)
    trend_traffic = pd.Series(traffic)
    trend_title = pd.Series(itemtitle)
    trend_link = pd.Series(itemlink)

    trend_pd = pd.DataFrame({'index': 'google', '검색어': trend_keywords, '내용': trend_title, '검색 수': trend_traffic,
                             '링크': trend_link})
    trend_pd.to_csv(file_name + '_' + rss_key + '.csv', encoding="utf-8")


url_list = {
    'KR':'https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR',
    'US':'https://trends.google.com/trends/trendingsearches/daily/rss?geo=US',
    'GB':'https://trends.google.com/trends/trendingsearches/daily/rss?geo=GB'
}

for key, url in url_list.items():
    getTrendsInfo(url, key)