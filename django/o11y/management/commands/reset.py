from django.core.management import BaseCommand

from o11y.models import Resource


class Command(BaseCommand):

    def handle(self, *args, **options):
        Resource.objects.all().delete()

