import requests
from django.shortcuts import render
from bs4 import BeautifulSoup, Comment


def get_html_content(request, slug=None):
    session = requests.Session()
    if slug == None:
        news = request.GET.get('news')
        news = news.replace(" ", "+")
        html_content = session.get(f'https://zaxid.net/search/search.do?searchValue={news}').text
    else:
        html_content = session.get(f'https://zaxid.net/{slug}').text

    return html_content

#fetch the data of the article from the news site
def collect_all_articles(soup):
    if soup.find("div", attrs={"class": "search_count_wrap"}).text == 'нічого не знайдено':
        return 'Nothing found'

    articels = []
    soup = soup.find("ul", attrs={"class": "list search_list"})
    for soup_article in soup.find_all("li"):
        article = dict()
        article['type'] = soup_article.find("span", attrs={"class": "type"}).text
        article['category'] = soup_article.find("a", attrs={"class": "category"}).text
        article['date'] = soup_article.find("span", attrs={"class": "date"}).text
        article['time'] = soup_article.find("span", attrs={"class": "time"}).text
        article['title'] = soup_article.find_next("div", attrs={"class": "title"}).text
        article['description'] = soup_article.find("div", attrs={"class": "desc"}).text
        article['slug'] = soup_article.find("div", attrs={"class": "title"}).find('a')['href'].split('https://zaxid.net/')[1]

        articels.append(article)

    return articels

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

#fetch the content of the article
def collect_data_of_article(soup):
    try:
        article = dict()
        b_img_soup = soup.find("div", attrs={"class": "b_photo"})
        if b_img_soup != None:
            article['img'] = b_img_soup.find("span").find("img")['srcset']

        article['category'] = soup.find("a", attrs={"class": "category"}).text
        article['time'] = soup.find("time", attrs={"class": "date"}).text
        article['title'] = soup.find("h1", attrs={"class": "title"}, id="newsName").text

        soup_text = soup.find("div", attrs={"class": "newsSummary"}, id="newsSummary")
        if soup.find("div", attrs={"class": "newsSummary"}, id="newsSummary") == None:
            soup_text = soup.find("div", id="newsSummary")

        if soup_text.find("div", attrs={"class": "subscribe-wrap"}) != None:
            unwanted = soup_text.find("div", attrs={"class": "subscribe-wrap"})
            unwanted.extract()

        texts = soup_text.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        article['article'] = u" ".join(t.strip() for t in visible_texts)
    except AttributeError:
        return '404'

    return article

def news_search(request):
    articles = None
    if 'news' in request.GET:
        html_content = get_html_content(request)
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = collect_all_articles(soup)

    if articles == 'Nothing found':
        nothing_found = 'Nothing found'
        return render(request, 'core/news_search.html', {'nothing_found': nothing_found})

    return render(request, 'core/news_search.html', {'articels': articles})

def article(request, slug):
    html_content = get_html_content(request, slug)
    soup = BeautifulSoup(html_content, 'html.parser')
    article = collect_data_of_article(soup)

    if article == '404':
        return render(request, 'core/404.html')

    return render(request, 'core/article.html', {'article': article})