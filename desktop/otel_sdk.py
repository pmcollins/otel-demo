from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

def prep_sdk_arg(parser):
    parser.add_argument('--sdk', action='store_true', default=False)

def conditionally_setup_otel_sdk(options):
    if options['sdk']:
        print('setting up otel sdk')
        setup_otel_sdk()
    else:
        print('NOT setting up otel sdk')

def setup_otel_sdk():
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(tracer_provider)
    metrics.set_meter_provider(MeterProvider(metric_readers=[(PeriodicExportingMetricReader(OTLPMetricExporter()))]))
