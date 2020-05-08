from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.article_list, name='article-list'),
]
