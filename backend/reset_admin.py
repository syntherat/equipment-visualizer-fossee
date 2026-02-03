#!/usr/bin/env python
"""
Reset admin user password directly
Run this from the backend directory with activated venv
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

try:
    # Try to get existing admin user
    user = User.objects.get(username='admin')
    print(f"✓ Found existing user: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Is staff: {user.is_staff}")
    print(f"  Is superuser: {user.is_superuser}")
except User.DoesNotExist:
    print("✗ No admin user found. Creating one...")
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print(f"✓ Created superuser: {user.username}")

# Reset password
password = input("\nEnter new password (press Enter for 'admin123'): ").strip() or 'admin123'
user.set_password(password)
user.save()
print(f"\n✓ Password reset successfully!")
print(f"  Username: {user.username}")
print(f"  Password: {password}")
print(f"\nTry logging in now with these credentials.")
