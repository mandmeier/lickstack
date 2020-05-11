from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.text import slugify
from blog.models import Article
#from django.http import HttpResponse
from . import forms


def article_list(request):
    articles = Article.objects.all().order_by('date_published')
    context = {}
    context['articles'] = articles
    return render(request, 'blog/article_list.html', context)


def article_detail(request, slug):
    article = Article.objects.get(slug=slug)
    context = {}
    context['article'] = article
    return render(request, 'blog/article_detail.html', context)


# import re

# def slugify(title):
#     title = title.lower()
#     title = re.sub(r'&', 'and', title)
#     title = re.sub(r'[\s\W]+', '-', title)
#     return title.strip('-')


@login_required
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            # save to db
            instance = form.save(commit=False)
            instance.author = request.user
            print(instance.title)
            instance.slug = slugify(instance.title)
            instance.save()
            return redirect('blog:article-list')
    else:
        form = forms.CreateArticle()
    context = {}
    context['form'] = form
    return render(request, 'blog/article_create.html', context)
