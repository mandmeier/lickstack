from django.urls import path
#from . import views
from .views import (
    home,
    browse_licks_view,
    my_licks_view,
    UserLickListView,
    #LickDetailView,
    LickCreateView,
    LickUpdateView,
    LickDeleteView,
    like_lick,
    lick_detail,
)

urlpatterns = [
    path('', home, name='home'),
    path('licks/', browse_licks_view, name='browse-licks'),
    path('mylicks/', my_licks_view, name='my-licks'),
    path('user/<str:username>/', UserLickListView.as_view(), name='user-licks'),
    #path('lick/<int:pk>/', LickDetailView.as_view(), name='lick-detail'),
    path('lick/<int:pk>/', lick_detail, name='lick-detail'),
    path('lick/new/', LickCreateView.as_view(), name='lick-create'),
    path('lick/<int:pk>/update/', LickUpdateView.as_view(), name='lick-update'),
    path('lick/<int:pk>/delete/', LickDeleteView.as_view(), name='lick-delete'),
    path(r'^like/$', like_lick, name='like_lick'),
]
