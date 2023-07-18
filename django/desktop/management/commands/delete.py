from django.core.management import BaseCommand

from desktop.models import Resource


class Command(BaseCommand):

    def handle(self, *args, **options):
        Resource.objects.all().delete()

