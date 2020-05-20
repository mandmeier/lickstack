from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from blog.models import Article
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote_plus
from . import forms


@login_required
def article_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

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


def article_detail(request, slug=None):
    article = get_object_or_404(Article, slug=slug)
    if article.draft or article.date_published > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(article.title)
    context = {}
    context['article'] = article
    context['share_string'] = share_string
    return render(request, 'blog/article_detail.html', context)


def article_list(request):
    today = timezone.now().date()
    queryset_list = Article.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        articles = Article.objects.all().order_by('-date_published')
    else:
        articles = Article.objects.active().order_by('-date_published')
        # active method defined in model manager

    query = request.GET.get("q")
    if query:
        articles = queryset_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(body__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    # paginate
    page = request.GET.get('page', 1)
    paginator = Paginator(articles, 2)
    articles = paginator.page(page)

    context = {}
    context['articles'] = articles
    context['today'] = today
    return render(request, 'blog/article_list.html', context)


def article_update(request, slug=None):
    article = get_object_or_404(Article, slug=slug)
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
    article = get_object_or_404(Article, slug=slug)
    article.delete()
    messages.success(request, 'Your article was successfully deleted.')
    return redirect('blog:article-list')
