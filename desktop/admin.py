from django.contrib import admin

from .models import NumberDataPoint, Resource, ResourceAttribute, ScopeMetrics, Metric, ScalarMetric

admin.site.register(Resource)
admin.site.register(ResourceAttribute)
admin.site.register(ScopeMetrics)
admin.site.register(Metric)
admin.site.register(ScalarMetric)
admin.site.register(NumberDataPoint)
