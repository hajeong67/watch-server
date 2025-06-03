from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Watch

User = get_user_model()

class Command(BaseCommand):
    help = "Create a user and register a watch with device_id"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the new user')
        parser.add_argument('device_id', type=str, help='Device ID for the watch')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        device_id = kwargs['device_id']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f"⚠️ User '{username}' already exists."))
        else:
            email = f"{username}@example.com"
            user = User.objects.create_user(username=username, email=email, password="1234")
            self.stdout.write(self.style.SUCCESS(f"✅ User '{username}' created."))

        if hasattr(user, 'watch'):
            self.stdout.write(self.style.WARNING(f"⚠️ User '{username}' already has a watch."))
        elif Watch.objects.filter(device_id=device_id).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ Device ID '{device_id}' is already registered."))
        else:
            Watch.objects.create(device_id=device_id, user=user)
            self.stdout.write(self.style.SUCCESS(f"✅ Watch '{device_id}' linked to user '{username}'"))
