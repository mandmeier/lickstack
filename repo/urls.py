from django.urls import path
from . import views
from .views import LickListView, LickDetailView, LickCreateView

urlpatterns = [
    path('', views.LickListView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('lick/<int:pk>/', views.LickDetailView.as_view(), name='lick-detail'),
    path('lick/new/', views.LickCreateView.as_view(), name='lick-create'),
    #path('lick/new/', views.lick_new, name='lick_new'),
    #path('', views.LickListView.as_view(), name='licks'),
    #path('lick/<uuid:pk>', views.LickDetailView.as_view(), name='lick-detail'),
]
