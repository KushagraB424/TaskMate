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
    role_counts = User.objects.values('role').annotate(count=Count('id'))
    
    data = {
        'status_labels': [item['status'] for item in status_counts],
        'status_data': [item['count'] for item in status_counts],
        
        'service_labels': [item['service__name'] for item in service_counts],
        'service_data': [item['count'] for item in service_counts],
        
        'role_labels': [item['role'] for item in role_counts],
        'role_data': [item['count'] for item in role_counts],
    }
    
    return JsonResponse(data)
