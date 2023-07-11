import hashlib
import json
import time
from concurrent import futures
from datetime import datetime

import grpc
import pytz
from django.core.management.base import BaseCommand
from opentelemetry import metrics
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2, metrics_service_pb2_grpc
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2, trace_service_pb2_grpc

from desktop.models import Resource, ResourceAttribute, ScopeMetrics, Metric, ScalarMetric, NumberDataPoint
from desktop.otel_sdk import setup_otel_sdk

DJANGO_INGEST_COMMAND = 'django.ingest.command'


class Command(BaseCommand):

    def handle(self, *args, **options):
        setup_otel_sdk()
        metrics.get_meter(DJANGO_INGEST_COMMAND, '1.0').create_counter('run.count', unit='{runs}').add(1)
        serve_otel_grpc()


def serve_otel_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    trace_service_pb2_grpc.add_TraceServiceServicer_to_server(TraceServiceServicer(), server)
    metrics_service_pb2_grpc.add_MetricsServiceServicer_to_server(MetricsServiceServicer(), server)
    server.add_insecure_port('0.0.0.0:4317')
    print('ingest starting...')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('stopping')
        server.stop(0)


class TraceServiceServicer(trace_service_pb2_grpc.TraceServiceServicer):

    def Export(self, request, context):
        print('TraceServiceServicer', time.time())
        print('request', request)
        return trace_service_pb2.ExportTraceServiceResponse()


class MetricsServiceServicer(metrics_service_pb2_grpc.MetricsServiceServicer):

    def __init__(self):
        meter = metrics.get_meter(DJANGO_INGEST_COMMAND, '1.0')
        self._counter = meter.create_counter('metrics.servicer.count', unit='{runs}')

    def Export(self, request, context):
        print('MetricsServiceServicer', time.time())
        self._counter.add(1)
        try:
            save_metrics(request.resource_metrics)
        except Exception as e:
            print('oops', e)
        return metrics_service_pb2.ExportMetricsServiceResponse()


def save_metrics(resource_metrics_proto):
    print('save metrics running')
    for resource_metric_proto in resource_metrics_proto:
        attr_dict = {}
        for kv_proto in resource_metric_proto.resource.attributes:
            attr_dict[kv_proto.key] = kv_proto.value.string_value
        attr_json = json.dumps(attr_dict, sort_keys=True)
        attr_hash = hashlib.sha256(attr_json.encode()).hexdigest()

        resource_model = select_or_insert_resource(attr_hash, resource_metric_proto.resource.attributes)

        for scope_metrics_proto in resource_metric_proto.scope_metrics:
            scope_model = select_or_insert_scope_metric(resource_model, scope_metrics_proto.scope.name)
            for metric_proto in scope_metrics_proto.metrics:
                metric = select_or_insert_metric(scope_model, metric_proto)
                if hasattr(metric_proto, 'sum'):
                    sm_model = select_or_insert_scalar_metric(metric, metric_proto.sum, 'sum')
                    for pt_proto in metric_proto.sum.data_points:
                        insert_point(sm_model, pt_proto)


def select_or_insert_resource(attributes_hash, proto_resource_attr_set):
    try:
        resource = Resource.objects.get(attributes_hash=attributes_hash)
    except Resource.DoesNotExist:
        resource = Resource(attributes_hash=attributes_hash)
        resource.save()
        for proto_resource_attr in proto_resource_attr_set:
            ResourceAttribute(
                key=proto_resource_attr.key,
                value=proto_resource_attr.value.string_value,
                resource=resource,
            ).save()
    return resource


def select_or_insert_scope_metric(resource, scope):
    existing_scope_metrics = resource.scopemetrics_set.filter(scope=scope)
    if len(existing_scope_metrics):
        scope_metric = existing_scope_metrics.first()
    else:
        scope_metric = ScopeMetrics(scope=scope, resource=resource)
        scope_metric.save()
    return scope_metric


def select_or_insert_metric(scope_model, metric_proto):
    existing_metrics = scope_model.metric_set.filter(name=metric_proto.name)
    if len(existing_metrics):
        metric = existing_metrics.first()
    else:
        metric = Metric(
            name=metric_proto.name,
            description=metric_proto.description,
            unit=metric_proto.unit,
            scope_metrics=scope_model,
        )
        metric.save()
    return metric


def select_or_insert_scalar_metric(metric, sum_proto, metric_type):
    scalar_metrics = metric.scalarmetric_set.filter(
        metric_type=metric_type,
        aggregation_temporality=sum_proto.aggregation_temporality,
        is_monotonic=sum_proto.is_monotonic,
    )
    if len(scalar_metrics):
        scalar_metric = scalar_metrics.first()
    else:
        scalar_metric = ScalarMetric(
            metric_type=metric_type,
            aggregation_temporality=sum_proto.aggregation_temporality,
            is_monotonic=sum_proto.is_monotonic,
            metric=metric
        )
        scalar_metric.save()
    return scalar_metric


def insert_point(sm_model, pt_proto):
    t = datetime.fromtimestamp(pt_proto.time_unix_nano / 1e9)
    z = pytz.timezone('UTC').localize(t)
    NumberDataPoint(
        time=z,
        int_value=pt_proto.as_int,
        scalar_metric=sm_model,
    ).save()