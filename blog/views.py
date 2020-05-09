from django.shortcuts import render
from blog.models import Article
from django.http import HttpResponse


def article_list(request):
    articles = Article.objects.all().order_by('date')
    context = {}
    context['articles'] = articles
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {}
    context['article'] = article
    return render(request, 'blog/article_detail.html', context)
