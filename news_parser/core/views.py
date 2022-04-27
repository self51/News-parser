import requests
from django.shortcuts import render
from bs4 import BeautifulSoup, SoupStrainer


def get_html_content(request):
    news = request.GET.get('news')
    news = news.replace(" ", "+")
    session = requests.Session()
    html_content = session.get(f'https://tsn.ua/ru/search?query=+{news}').text
    return html_content

#fetch the data of the article from the news site
def collect_all_articles(soup):
    articels = []
    soup = soup.find("div", attrs={"class": "c-feed-log--y c-feed-log--y-start"}, id="loadmore")
    for soup_article in soup.find_all("article"):
        article = dict()
        article['time'] = soup_article.find("time").text
        article['link_to_article'] = soup_article.find("a", attrs={"class": "c-card__link"}).text
        article['header_article'] = soup_article.find("a", attrs={"class": "c-card__link"})['href']
        article['img'] = soup_article.find("img")['data-src']
        articels.append(article)

    return articels

def news_search(request):
    articles = None
    if 'news' in request.GET:
        html_content = get_html_content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = collect_all_articles(soup)

    return render(request, 'core/news_search.html', {'articels': articles})

def article(request):
    pass