from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from blog.models import Article
from repo.models import Lick
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote_plus
from . import forms

from comments.forms import CommentForm
from comments.models import Comment


@login_required
def article_create(request):
    if not request.user.is_staff:
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
        parent_url = new_comment.content_object.get_absolute_url()
        redirect_url = f'{parent_url}#comments_section'
        return HttpResponseRedirect(redirect_url)

    comments = article.comments

    # get next object among published articles
    today = timezone.now().date()
    articles = Article.objects.all().order_by('pk').filter(
        draft=False).filter(date_published__lte=today)

    # get next 3 articles for preview
    def get_next_3(article):
        next_3 = articles[0:3]  # default
        for index, art in enumerate(articles):
            if art == article:
                next_3 = articles[index + 1:index + 4]
        if len(next_3) == 2:
            next_3 = next_3 + [articles[0]]
        if len(next_3) == 1:
            next_3 = next_3 + articles[0:2]
        if len(next_3) == 0:
            next_3 = articles[0:2] + [articles[7]]
        return next_3

    next_articles = get_next_3(article)

    context = {}
    context['article'] = article
    context['share_string'] = share_string
    context['comments'] = comments
    context['comment_form'] = form
    context['next_articles'] = next_articles

    # find licks if article has licks
    if article.lick_string and article.lick_string != '':
        lick_string = article.lick_string
        transpose_string = article.transpose_string

        lick_sequence = lick_string.split(',')

        licks = []
        for id in lick_sequence:
            try:
                lick = Lick.objects.get(id=id)
                licks.append(lick)
            except Lick.DoesNotExist:
                if request.user.is_staff:
                    messages.warning(request, f'Lick {id} not found!')
                # placeholder?

        context['transpose_string'] = transpose_string
        context['licks'] = licks

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
    paginator = Paginator(articles, 6)
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
