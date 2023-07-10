from django.shortcuts import render
from desktop.models import Resource, Metric, ScopeMetrics


def index(request):
    return render(
        request,
        'desktop/index.html',
        {'scope_metrics': ScopeMetrics.objects.all()}
    )
