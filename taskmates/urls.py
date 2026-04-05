from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-analytics/', views.admin_analytics_api, name='admin_analytics_api'),
    path('users/', include('users.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('customers/', include('customers.urls')),
    path('servicers/', include('servicers.urls')),
    # Landing page view
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
]
