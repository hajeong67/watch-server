from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Watch

User = get_user_model()

class Command(BaseCommand):
    help = 'User와 Watch 등록'

    def handle(self, *args, **kwargs):
        username = 'user_1'
        password = '1111'
        device_id = 'watch-id-001'
        email = f'{username}@example.com'

        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email}
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ 유저 생성: {username}'))
        else:
            self.stdout.write(f'ℹ️ 이미 존재: {username}')

        watch, created = Watch.objects.get_or_create(user=user, device_id=device_id)
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ 워치 등록 완료: {device_id}'))
        else:
            self.stdout.write(f'ℹ️ 이미 존재: {device_id}')
