from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from customers.models import ServiceRequest
from django.views.decorators.http import require_POST

@login_required
def dashboard_view(request):
    assigned_jobs = ServiceRequest.objects.filter(servicer=request.user).order_by('-request_date')
    open_jobs = ServiceRequest.objects.filter(status='PENDING', servicer__isnull=True).order_by('-request_date')

    return render(request, 'servicers/dashboard.html', {
        'assigned_jobs': assigned_jobs,
        'open_jobs': open_jobs,
    })

@login_required
@require_POST
def accept_job(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id, status='PENDING')
    job.servicer = request.user
    job.status = 'ACCEPTED'
    job.save()
    return redirect('servicer_dashboard')

@login_required
@require_POST
def complete_job(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id, servicer=request.user)
    job.status = 'COMPLETED'
    job.save()
    return redirect('servicer_dashboard')
