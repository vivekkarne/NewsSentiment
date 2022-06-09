from urllib import response
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
# from time import sleep
from time import time
import pandas as pd
import plotly.express as px

# import json


#keeps the lexicon upto date
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

recent_count = 10

def send_request():
    response = requests.get("https://www.aljazeera.com/where/mozambique/")
    data = response.text
    #Removing soft-hyphens from html
    data = data.replace('\xad', '')
    data = data.replace('\u00ad', '')
    data = data.replace('\N{SOFT HYPHEN}', '')
    return data

def pre_process(raw_list):
    processed_list = []
    for article in tqdm(raw_list, desc="Pre-processing articles"):
        title = article.select('h3.gc__title > a > span')[0]
        body = article.select('div.gc__excerpt > p')[0]
        processed_list.append({'title': title.text, 'body': body.text})
        #just to show tqdm
        # sleep(0.1)

    # generate data.json
    # with open('data.json', 'w',encoding='utf-8') as fout:
    #     json.dump(processed_list, fout,ensure_ascii=False, indent=4)
    return processed_list

def scrape(response_body):
    soup = BeautifulSoup(response_body, 'lxml')

    # top 4 articles
    featured_list = soup.find("ul", class_="featured-articles-list")
    featured_list_items = featured_list.find_all("li", class_="featured-articles-list__item")

    # remaining top 6 articles
    rem = recent_count - len(featured_list)
    news_feed = soup.find('section', id='news-feed-container')
    news_feed_articles = news_feed.find_all('article')[:rem]
    return featured_list_items + news_feed_articles

def sentiment_analysis(processed_data):
    #VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    for data in processed_data:
        scores = sid.polarity_scores(data['title']+'. '+data['body'])
        if scores['compound'] > 0:
            data['sentiment'] = 'positive'
        elif scores['compound'] < 0:
            data['sentiment'] = 'negative'
        else:
            data['sentiment'] = 'neutral'
    return processed_data

def u_plot(analyzed_data):
    #data to pandas dataframe
    df = pd.DataFrame(analyzed_data)

    #get count of articles by sentiment
    df1 = df.groupby('sentiment').agg(article_count=('sentiment','count'))
    df1 = df1.reset_index()

    #plot the bar graph
    fig = px.bar(df1, x='sentiment', y='article_count', title="Sentiment of articles")
    fig.show()
    # fig.write_image("plot.png")

def main():
    # start = time()
    response_body = send_request()
    raw_data = scrape(response_body)
    processed_data = pre_process(raw_data)
    analyzed_data = sentiment_analysis(processed_data)
    u_plot(analyzed_data)
    # end = time()
    # print(end-start)

if __name__ == "__main__":
    main()