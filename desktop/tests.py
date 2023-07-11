import pickle

from django.test import TestCase

from desktop.management.commands.ingest import save_metrics
from desktop.models import Resource


class IngestTest(TestCase):

    def test_save_metrics(self):
        request = unpickle_request()
        save_metrics(request.resource_metrics)

        resources = Resource.objects.all()
        self.assertEquals(len(resources), 1)
        resource = resources.first()
        self.assertTrue(len(resource.attributes_hash) > 0)
        scope_metrics = resource.scopemetrics_set.all()
        self.assertEquals(1, len(scope_metrics))
        scope_metric = scope_metrics.first()
        self.assertEquals('ingest-metrics', scope_metric.scope)
        metrics = scope_metric.metric_set.all()
        self.assertEquals(1, len(metrics))
        metric = metrics.first()
        self.assertEquals('ingest-metrics.run.count', metric.name)
        self.assertEquals('{runs}', metric.unit)
        scalar_metrics = metric.scalarmetric_set.all()
        self.assertEquals(1, len(scalar_metrics))
        scalar_metric = scalar_metrics.first()
        self.assertEquals(True, scalar_metric.is_monotonic)
        self.assertEquals('sum', scalar_metric.metric_type)
        self.assertEquals(2, scalar_metric.aggregation_temporality)
        points = scalar_metric.numberdatapoint_set.all()
        self.assertEquals(1, len(points))
        point = points.first()
        self.assertEquals(1, point.int_value)


def pickle_request(request):
    with open('desktop/test_metrics_request.pkl', 'wb') as f:
        pickle.dump(request, f)


def unpickle_request():
    with open('desktop/test_metrics_request.pkl', 'rb') as f:
        return pickle.load(f)
