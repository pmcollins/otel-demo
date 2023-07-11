from django.core.management import BaseCommand
from opentelemetry import metrics

from desktop.models import Metric
from desktop.otel_sdk import conditionally_setup_otel_sdk, prep_sdk_arg


class Command(BaseCommand):

    def add_arguments(self, parser):
        prep_sdk_arg(parser)
        parser.add_argument('metric_name', type=str)

    def handle(self, *args, **options):
        conditionally_setup_otel_sdk(options)

        meter = metrics.get_meter('django.command.query')
        counter = meter.create_counter('query.count')
        counter.add(1)

        metric_name = options['metric_name']
        print('metric_name', metric_name)
        found = Metric.objects.filter(name=metric_name)
        print(len(found))
