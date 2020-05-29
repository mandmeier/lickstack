from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^comments/(?P<id>\d+)/$',
        views.comment_thread, name='thread'),
    url(r'^comments/(?P<id>\d+)/delete/$',
        views.comment_delete, name='comment-delete'),
]
