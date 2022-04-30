import requests
from django.shortcuts import render
from bs4 import BeautifulSoup, SoupStrainer


def get_html_content(request, slug=None):
    session = requests.Session()
    if slug == None:
        news = request.GET.get('news')
        news = news.replace(" ", "+")
        html_content = session.get(f'https://tsn.ua/ru/search?query=+{news}').text
    else:
        category = slug.split('-')[0]
        slug_without_category = slug.split('-', 1)[1]
        html_content = session.get(f'https://tsn.ua/ru/{category}/{slug_without_category}').text

    return html_content

#fetch the data of the article from the news site
def collect_all_articles(soup):
    articels = []
    soup = soup.find("div", attrs={"class": "c-feed-log--y c-feed-log--y-start"}, id="loadmore")
    for soup_article in soup.find_all("article"):
        article = dict()
        article['time'] = soup_article.find("time").text
        article['header_article'] = soup_article.find("a", attrs={"class": "c-card__link"}).text
        article['img'] = soup_article.find("img")['data-src']

        link_to_article = soup_article.find("a", attrs={"class": "c-card__link"})['href']
        slug = link_to_article.split('ru/')[1]
        slug_combined_category = slug.replace("/", "-")
        article['slug'] = slug_combined_category

        articels.append(article)

    return articels

def news_search(request):
    articles = None
    if 'news' in request.GET:
        html_content = get_html_content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = collect_all_articles(soup)

    return render(request, 'core/news_search.html', {'articels': articles})

def article(request, slug):
    article = dict()
    html_content = get_html_content(request, slug)
    article['html_content'] = html_content

    return render(request, 'core/article.html', {'article': article})