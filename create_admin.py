import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmates.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("SUCCESS: Admin user created. Username: admin, Password: admin")
else:
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print("SUCCESS: Admin user password reset. Username: admin, Password: admin")
