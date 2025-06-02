from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Watch

class Command(BaseCommand):
    help = '테스트용 watch_user와 Watch 등록'

    def handle(self, *args, **kwargs):
        username = 'watch_user'
        password = 'watch_pass'
        device_id = 'test-watch-id-001'

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ 유저 생성: {username}'))

        watch, created = Watch.objects.get_or_create(user=user, device_id=device_id)
        if created:
            self.stdout.write(self.style.SUCCESS(f'✅ 워치 등록 완료: {device_id}'))
        else:
            self.stdout.write(f'ℹ️ 이미 존재: {device_id}')
