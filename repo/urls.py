from django.urls import path
#from . import views
from .views import (
    about,
    LickListView,
    UserLickListView,
    LickDetailView,
    LickCreateView,
    LickUpdateView,
    LickDeleteView
)

urlpatterns = [
    path('', LickListView.as_view(), name='home'),
    path('user/<str:username>/', UserLickListView.as_view(), name='user-licks'),
    path('about/', about, name='about'),
    path('lick/<int:pk>/', LickDetailView.as_view(), name='lick-detail'),
    path('lick/new/', LickCreateView.as_view(), name='lick-create'),
    path('lick/<int:pk>/update/', LickUpdateView.as_view(), name='lick-update'),
    path('lick/<int:pk>/delete/', LickDeleteView.as_view(), name='lick-delete'),
]
