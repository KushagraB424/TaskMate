from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='customer_dashboard'),
    path('book/<int:service_id>/', views.book_service, name='book_service'),
]
