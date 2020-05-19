from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.article_list, name='article-list'),
    path('blog/article/create/', views.article_create, name='article-create'),
    url(r'^blog/article/(?P<id>\d+)/$',
        views.article_detail, name='article-detail'),
    url(r'^blog/article/(?P<id>\d+)/edit/$',
        views.article_update, name='article-update'),
    url(r'^blog/article/(?P<id>\d+)/delete/$',
        views.article_delete, name='article-delete'),
]
