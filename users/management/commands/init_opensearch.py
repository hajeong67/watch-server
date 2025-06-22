from django.core.management.base import BaseCommand
from watch.opensearch_setup import init_opensearch

class Command(BaseCommand):
    help = "Set up OpenSearch (ILM policy, index template, data stream)"

    def handle(self, *args, **options):
        init_opensearch()
        self.stdout.write(self.style.SUCCESS("OpenSearch 초기화 완료"))
