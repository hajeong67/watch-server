# management/commands/delete_pg_user.py
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "PostgreSQL 사용자 삭제 (종속성 제거 포함)"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']

        with connection.cursor() as cursor:
            # 활성 세션 종료
            cursor.execute(f"""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE usename = '{username}'
            """)

            # 종속 객체 제거
            cursor.execute(f"DROP OWNED BY {username}")
            cursor.execute(f"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {username}")

            # 사용자 삭제
            cursor.execute(f"DROP USER IF EXISTS {username}")

        self.stdout.write(f"User {username} 삭제 완료!")
