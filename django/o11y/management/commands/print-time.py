import time
from datetime import datetime

from django.core.management import BaseCommand
from opentelemetry import metrics

from o11y.otel_sdk import conditionally_setup_otel_sdk, prep_sdk_arg


class Command(BaseCommand):

    def add_arguments(self, parser):
        prep_sdk_arg(parser)

    def handle(self, *args, **options):
        conditionally_setup_otel_sdk(options)

        meter = metrics.get_meter('django.command.print-time')
        meter.create_counter('run.count').add(1)
        print_counter = meter.create_counter('print.count')

        while True:
            time.sleep(1)
            print_counter.add(1)
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
