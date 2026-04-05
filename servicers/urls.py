from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='servicer_dashboard'),
    path('job/<int:job_id>/accept/', views.accept_job, name='accept_job'),
    path('job/<int:job_id>/complete/', views.complete_job, name='complete_job'),
]
