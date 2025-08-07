from django.urls import path
from .views import PublicUserDetailView

urlpatterns = [
    path('<str:username>/', PublicUserDetailView.as_view(), name='user-detail'),
]
