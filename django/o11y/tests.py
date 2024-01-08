import pickle

from django.test import TestCase

from o11y.management.commands.ingest import save_metrics, save_logs, get_pickle_fname, save_spans
from o11y.models import Resource, Span


class IngestTest(TestCase):

    def test_save_metrics(self):
        request = unpickle_metrics_request()
        save_metrics(request.resource_metrics)

        resources = Resource.objects.all()
        self.assertEquals(len(resources), 1)
        resource = resources.first()
        self.assertTrue(len(resource.attributes_hash) > 0)
        scope_metrics_queryset = resource.scopemetrics_set.all()
        self.assertEquals(1, len(scope_metrics_queryset))
        scope_metrics = scope_metrics_queryset.first()
        self.assertEquals('ingest-metrics', scope_metrics.scope)
        scope_metrics_queryset = scope_metrics.metric_set.all()
        self.assertEquals(1, len(scope_metrics_queryset))
        metric = scope_metrics_queryset.first()
        self.assertEquals('ingest-metrics.run.count', metric.name)
        self.assertEquals('{runs}', metric.unit)
        scalar_metrics_queryset = metric.scalarmetric_set.all()
        self.assertEquals(1, len(scalar_metrics_queryset))
        scalar_metric = scalar_metrics_queryset.first()
        self.assertEquals(True, scalar_metric.is_monotonic)
        self.assertEquals('sum', scalar_metric.metric_type)
        self.assertEquals(2, scalar_metric.aggregation_temporality)
        point_queryset = scalar_metric.numberdatapoint_set.all()
        self.assertEquals(1, len(point_queryset))
        point = point_queryset.first()
        self.assertEquals(1, point.int_value)

    def test_save_logs(self):
        request = unpickle_logs_request()
        save_logs(request.resource_logs)

        resources = Resource.objects.all()
        self.assertEquals(len(resources), 1)
        resource = resources.first()
        self.assertTrue(len(resource.attributes_hash) > 0)

        scope_logs_queryset = resource.scopelogs_set.all()
        self.assertTrue(len(scope_logs_queryset) > 0)
        scope_logs = scope_logs_queryset.first()
        self.assertEquals('opentelemetry.sdk._logs._internal', scope_logs.scope)
        log_record_queryset = scope_logs.logrecord_set.all()
        self.assertTrue(len(log_record_queryset) == 1)
        log_record = log_record_queryset.first()
        self.assertEquals('error', log_record.body)
        self.assertEquals(17, log_record.severity_number)
        self.assertEquals('ERROR', log_record.severity_text)
        self.assertTrue(log_record.time is not None)

    def test_save_spans(self):
        request = unpickle_trace_request()
        save_spans(request.resource_spans)
        spans = Span.objects.all()
        model_span = spans[0]
        proto_span = request.resource_spans[0].scope_spans[0].spans[0]
        assert model_span.trace_id == str(proto_span.trace_id)
        assert model_span.span_id == str(proto_span.span_id)


def unpickle_metrics_request():
    return unpickle_request('metrics')


def unpickle_logs_request():
    return unpickle_request('logs')


def unpickle_trace_request():
    return unpickle_request('trace')


def unpickle_request(telemetry_type):
    with open(get_pickle_fname(telemetry_type), 'rb') as f:
        return pickle.load(f)
