import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmates.settings')
django.setup()

from services.models import Category, ServiceListing

cat_cleaning, _ = Category.objects.get_or_create(name='Cleaning', description='Home cleaning services')
cat_repair, _ = Category.objects.get_or_create(name='Repair', description='Home appliance and furniture repair')

ServiceListing.objects.get_or_create(
    category=cat_cleaning,
    name='Deep House Cleaning',
    description='A thorough cleaning of all rooms including bathrooms, kitchen, and floors.',
    base_price=120.00
)

ServiceListing.objects.get_or_create(
    category=cat_cleaning,
    name='Sofa Steam Wash',
    description='Professional machine dry cleaning and stain removal applied to a standard 3-seater sofa.',
    base_price=45.00
)

ServiceListing.objects.get_or_create(
    category=cat_repair,
    name='Air Conditioning Repair',
    description='Comprehensive maintenance of window or split AC units including a high-pressure wash and fluid check.',
    base_price=65.00
)

ServiceListing.objects.get_or_create(
    category=cat_repair,
    name='Emergency Plumbing',
    description='Urgent visit from a skilled technician to diagnose and repair pipes, faucets, or drainage blocks.',
    base_price=55.00
)

print("SUCCESS: Demo Database Data Seeded!")
