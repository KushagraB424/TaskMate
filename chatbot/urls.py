from django.urls import path
from .views import ChatQueryView

urlpatterns = [
    path('query/', ChatQueryView.as_view(), name='chat_query'),
]
