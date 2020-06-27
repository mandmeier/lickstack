from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('all-articles/', views.article_list, name='article-list'),
    path('article/create/', views.article_create, name='article-create'),
    url(r'^article/(?P<slug>[\w-]+)/$',
        views.article_detail, name='article-detail'),
    url(r'^article/(?P<slug>[\w-]+)/edit/$',
        views.article_update, name='article-update'),
    url(r'^article/(?P<slug>[\w-]+)/delete/$',
        views.article_delete, name='article-delete'),
]
