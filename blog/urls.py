from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/', views.article_list, name='article-list'),
    path('blog/create/', views.article_create, name='article-create'),
    url(r'^blog/(?P<slug>[\w-]+)/$',
        views.article_detail, name='article-detail'),
]
