import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmates.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Look for kushagraadmin
user = User.objects.filter(username='kushagraadmin').first()
if user:
    user.is_staff = True
    user.is_superuser = True
    user.role = 'ADMIN'
    user.save()
    print("SUCCESS: kushagraadmin has been promoted to a Superuser!")
else:
    print("ERROR: User kushagraadmin does not exist. Did you spell it correctly?")
