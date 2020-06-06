from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from blog.models import Article
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote_plus
from . import forms

from comments.forms import CommentForm
from comments.models import Comment


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

    initial_data = {
        "content_type": article.get_content_type,
        "object_id": article.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            author=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data,
            parent=parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = article.comments

    #licks = article.licks.all()

    transpose_string = "1|5,2|3,2|4"

    lick_sequence = [1, 2, 2]

    licks = []
    for id in lick_sequence:
        lick = article.licks.get(id=id)
        licks.append(lick)
        print(lick)

    context = {}
    context['article'] = article
    context['share_string'] = share_string
    context['comments'] = comments
    context['comment_form'] = form
    context['licks'] = licks
    context['transpose_string'] = transpose_string
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
    paginator = Paginator(articles, 10)
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
