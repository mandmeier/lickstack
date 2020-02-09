from django.urls import path
#from . import views
from .views import (
    home,
    browse_licks_view,
    LickListView,
    UserLickListView,
    LickDetailView,
    LickCreateView,
    LickUpdateView,
    LickDeleteView,
)

urlpatterns = [
    path('', home, name='home'),
    path('licks/', browse_licks_view, name='browse-licks'),
    path('all/', LickListView.as_view(), name='all-licks'),
    path('user/<str:username>/', UserLickListView.as_view(), name='user-licks'),
    path('lick/<int:pk>/', LickDetailView.as_view(), name='lick-detail'),
    path('lick/new/', LickCreateView.as_view(), name='lick-create'),
    path('lick/<int:pk>/update/', LickUpdateView.as_view(), name='lick-update'),
    path('lick/<int:pk>/delete/', LickDeleteView.as_view(), name='lick-delete'),
]
