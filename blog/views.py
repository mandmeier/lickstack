from django.shortcuts import render
from blog.models import Article


def article_list(request):
    articles = Article.objects.all().order_by('date')
    context = {}
    context['articles'] = articles
    return render(request, 'blog/article_list.html', context)
