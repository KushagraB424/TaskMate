from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from customers.models import ServiceRequest
from django.db.models import Count, Sum
from django.contrib.auth import get_user_model

@staff_member_required
def admin_analytics_api(request):
    User = get_user_model()
    
    # Existing Bookings by Status
    status_counts = ServiceRequest.objects.values('status').annotate(count=Count('status'))
    # Existing Bookings by Service Type
    service_counts = ServiceRequest.objects.values('service__name').annotate(count=Count('id'))
    
    # NEW: Users by Role
    # NEW: Users by Role
    role_counts = User.objects.values('role').annotate(count=Count('id'))
    
    # NEW: Average Rating by Provider
    from customers.models import Review
    from django.db.models import Avg
    
    providers = User.objects.filter(role='SERVICER')
    provider_names = []
    provider_ratings = []
    
    for provider in providers:
        avg = Review.objects.filter(service_request__servicer=provider).aggregate(Avg('rating'))['rating__avg']
        if avg is not None:
            provider_names.append(provider.username)
            provider_ratings.append(round(avg, 2))
    
    data = {
        'status_labels': [item['status'] for item in status_counts],
        'status_data': [item['count'] for item in status_counts],
        
        'service_labels': [item['service__name'] for item in service_counts],
        'service_data': [item['count'] for item in service_counts],
        
        'role_labels': [item['role'] for item in role_counts],
        'role_data': [item['count'] for item in role_counts],
        
        'provider_labels': provider_names,
        'provider_ratings': provider_ratings,
    }
    
    return JsonResponse(data)
