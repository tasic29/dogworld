from django.urls import path
from .views import PublicUserDetailView, search_users

urlpatterns = [
    path('search/', search_users, name='search_users'),
    path('<str:username>/', PublicUserDetailView.as_view(), name='user-detail'),
]
