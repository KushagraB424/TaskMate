import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import ServiceRequest, Review

@admin.action(description='Export Selected Requests as CSV')
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="service_requests.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Customer', 'Servicer', 'Service', 'Status', 'Request Date'])
    for obj in queryset:
        writer.writerow([
            obj.id,
            obj.customer.username if obj.customer else '',
            obj.servicer.username if obj.servicer else '',
            obj.service.name if obj.service else '',
            obj.status,
            obj.request_date
        ])
    return response

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'servicer', 'service', 'status', 'request_date')
    list_filter = ('status',)
    actions = [export_as_csv]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'rating', 'created_at')
