import json
import urllib.request
import requests
import httpx

from django.http import JsonResponse
from django.shortcuts import render

from desktop.models import ScopeMetrics


def index(request):
    return render(request, 'desktop/index.html')

def metrics(request):
    return render(
        request,
        'desktop/metrics.html',
        {'scope_metrics': ScopeMetrics.objects.all()}
    )

def fastapi(request):
    with urllib.request.urlopen('http://localhost:8001') as resp:
        thing = json.loads(resp.read())
    return JsonResponse(thing)

def flask(request):
    resp = requests.get('http://localhost:8002')
    return JsonResponse(json.loads(resp.text))

def bottle(request):
    resp = httpx.get('http://localhost:8003')
    return JsonResponse(resp.json())
