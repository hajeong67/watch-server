# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.management import call_command
from django.core.exceptions import PermissionDenied
import logging
from config import settings
from watch.opensearch_client import client

logger = logging.getLogger(__name__)
INDEX_NAME = settings.OPENSEARCH_INDEX_NAME

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)


class Watch(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="watch",
        db_constraint=False
    )


@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    """사용자 삭제 시 PostgreSQL 사용자 + OpenSearch 데이터 동기 삭제"""
    try:
        # 1. PostgreSQL 사용자 삭제
        call_command('delete_pg_user', instance.username, verbosity=0)

        # 2. OpenSearch 데이터 삭제
        if hasattr(instance, 'watch'):
            device_id = instance.watch.device_id

            # OpenSearch에서 해당 device_id를 가진 모든 문서 삭제
            query = {"query": {"match": {"device_id": device_id}}}
            response = client.delete_by_query(
                index=INDEX_NAME,
                body=query,
                refresh=True  # 즉시 색인 갱신
            )

            logger.info(f"OpenSearch 데이터 삭제 완료: {response}")
            instance.watch.delete()

    except Exception as e:
        logger.error(f"데이터 삭제 실패: {str(e)}", exc_info=True)
        if not settings.DEBUG:
            raise PermissionDenied("데이터 삭제 중 오류 발생") from e
