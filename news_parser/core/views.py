from django.shortcuts import render

from .service import Parser


def news_search(request):
    articles = None

    if 'news' in request.GET:
        p = Parser()
        news = request.GET.get('news')
        articles = p.collect_all_articles(news)

    if articles == '404':
        return render(request, 'core/404.html')
    elif articles == 'Nothing found':
        nothing_found = 'Nothing found'
        return render(request, 'core/news_search.html', {'nothing_found': nothing_found})

    return render(request, 'core/news_search.html', {'articels': articles})

def article(request, slug):
    p = Parser()
    article = p.collect_data_of_article(slug)

    if article == '404':
        return render(request, 'core/404.html')

    return render(request, 'core/article.html', {'article': article})