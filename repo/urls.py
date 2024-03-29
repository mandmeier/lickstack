from django.urls import path
from .views import (
    home,
    browse_licks_view,
    my_licks_view,
    create_lick,
    like_lick,
    LickUpdateView,
    favorite_lick,
    lick_detail,
    delete_lick,
)

urlpatterns = [
    path('', home, name='home'),
    path('licks/', browse_licks_view, name='browse-licks'),
    path('mylicks/', my_licks_view, name='my-licks'),
    path('lick/new/', create_lick, name='lick-create'),
    path('lick/<int:pk>/update/', LickUpdateView.as_view(), name='lick-update'),
    path(r'^like/$', like_lick, name='like_lick'),
    path(r'^favorite/$', favorite_lick, name='favorite_lick'),
    path('lick/<int:pk>/', lick_detail, name='lick-detail'),
    path('lick/<int:pk>/delete/', delete_lick, name='lick-delete'),
]
