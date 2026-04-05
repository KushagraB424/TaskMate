from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from services.models import Category, ServiceListing
from customers.models import ServiceRequest

@login_required
def dashboard_view(request):
    services = ServiceListing.objects.filter(is_active=True)
    history = ServiceRequest.objects.filter(customer=request.user).order_by('-request_date')
    return render(request, 'customers/dashboard.html', {
        'services': services,
        'history': history
    })

@login_required
def book_service(request, service_id):
    if request.method == 'POST':
        service = get_object_or_404(ServiceListing, id=service_id)
        address = request.POST.get('address')
        scheduled_date = request.POST.get('scheduled_date')
        ServiceRequest.objects.create(
            customer=request.user,
            service=service,
            status='PENDING',
            address=address,
            scheduled_date=scheduled_date
        )
    return redirect('customer_dashboard')
