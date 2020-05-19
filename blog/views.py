from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from blog.models import Article
from django.http import HttpResponse, HttpResponseRedirect
from . import forms


@login_required
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST or None, request.FILES or None)
        if form.is_valid():
            # save to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            messages.success(
                request, 'Your article has been successfully created')
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        form = forms.CreateArticle()
    context = {}
    context['form'] = form
    return render(request, 'blog/article_create.html', context)


def article_detail(request, id=None):
    article = get_object_or_404(Article, id=id)
    context = {}
    context['article'] = article
    return render(request, 'blog/article_detail.html', context)


def article_list(request):
    articles = Article.objects.all().order_by('-date_published')

    # paginate
    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 8)
    articles = paginator.page(page)

    context = {}
    context['articles'] = articles
    return render(request, 'blog/article_list.html', context)


def article_update(request, id=None):
    article = get_object_or_404(Article, id=id)
    form = forms.CreateArticle(
        request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Your article has been successfully updated')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {}
    context['article'] = article
    context['form'] = form
    return render(request, 'blog/article_create.html', context)


def article_delete(request, id=None):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, 'Your article was successfully deleted.')
    return redirect('blog:article-list')
