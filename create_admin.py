import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
django.setup()

from users.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123', role='ADMIN')
        print("Superuser 'admin' created with password 'admin123'")
    else:
        print("Superuser 'admin' already exists")
        # Reset password just in case
        u = User.objects.get(username='admin')
        u.set_password('admin123')
        u.role = 'ADMIN'
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print("Password for 'admin' reset to 'admin123'")
except Exception as e:
    print(f"Error: {e}")
