import hashlib
import json

from django.db import models


# Resource -> ResourceAttribute
# Resource -> ScopeMetrics -> Metric -> ScalarMetric -> NumberDataPoint

class Resource(models.Model):
    attributes_hash = models.CharField(max_length=256, unique=True)

    def attributes_as_json(self):
        return attribute_set_to_json(self.resourceattribute_set.all())


class ResourceAttribute(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.key}: {self.value}'


class ScopeMetrics(models.Model):
    scope = models.CharField(max_length=256)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return self.scope


class Metric(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    unit = models.CharField(max_length=32)
    scope_metrics = models.ForeignKey(ScopeMetrics, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class ScalarMetric(models.Model):
    metric_type = models.CharField(max_length=256)  # gauge or sum
    aggregation_temporality = models.IntegerField()
    is_monotonic = models.BooleanField()
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)


class NumberDataPoint(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    time = models.DateTimeField()
    int_value = models.IntegerField(default=0)
    scalar_metric = models.ForeignKey(ScalarMetric, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.int_value}"


def scalar_metric_to_map_key(sm):
    return f"{sm.metric_type}_{sm.aggregation_temporality}_{sm.is_monotonic}"


def attribute_set_to_hash(attribute_set):
    json_str = attribute_set_to_json(attribute_set)
    return hashlib.sha256(json_str.encode()).hexdigest()


def attribute_set_to_json(attribute_set):
    return json.dumps({el.key: el.value for el in attribute_set}, sort_keys=True)
