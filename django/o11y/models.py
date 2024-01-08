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


class ScopeSpans(models.Model):
    scope = models.CharField(max_length=256)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return self.scope


class Span(models.Model):
    scope_spans = models.ForeignKey(ScopeSpans, on_delete=models.CASCADE)
    # 32 hexadecimal digits (16 bytes)
    trace_id = models.CharField(max_length=32)
    # 16 hexadecimal digits (8 bytes)
    span_id = models.CharField(max_length=16)
    name = models.CharField(max_length=256)

    class Kind(models.IntegerChoices):
        UNSPECIFIED = 0, 'Unspecified'
        INTERNAL = 1, 'Internal'
        SERVER = 2, 'Server'
        CLIENT = 3, 'Client'
        PRODUCER = 4, 'Producer'
        CONSUMER = 5, 'Consumer'

    kind = models.IntegerField(choices=Kind.choices)


# trace_id: ">(\364>\212[b\273\337/\027\014\311\n}\233"
# span_id: "L\225g\026b\270|\025"
# name: "GET index"
# kind: SPAN_KIND_SERVER
# start_time_unix_nano: 1704744559938028000
# end_time_unix_nano: 1704744559951359000

class ScopeMetrics(models.Model):
    scope = models.CharField(max_length=256)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return self.scope


class ScopeLogs(models.Model):
    scope = models.CharField(max_length=256)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)


class LogRecord(models.Model):
    time = models.DateTimeField(null=True, blank=True)
    severity_number = models.IntegerField()
    severity_text = models.CharField(max_length=256)
    body = models.TextField()
    trace_id = models.CharField(max_length=256)
    span_id = models.CharField(max_length=256)
    scope_logs = models.ForeignKey(ScopeLogs, on_delete=models.CASCADE)


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
