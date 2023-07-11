import time

from django.core.management import BaseCommand
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

meter_provider = MeterProvider(metric_readers=[(PeriodicExportingMetricReader(OTLPMetricExporter()))])
meter = meter_provider.get_meter('django.hello.command')
counter = meter.create_counter('hello.count')


class Command(BaseCommand):

    def handle(self, *args, **options):
        for x in range(1, 100):
            time.sleep(1)
            counter.add(1)
            print('hello')

