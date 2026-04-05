from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('customers/', include('customers.urls')),
    path('servicers/', include('servicers.urls')),
    # Landing page view
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
]
