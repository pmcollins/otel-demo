import json
import urllib.request
import requests
import httpx

from django.http import JsonResponse
from django.shortcuts import render

from o11y.models import ScopeMetrics, ScopeSpans


def index(req):
    return render(req, 'o11y/index.html')

def metrics(req):
    return render(
        req,
        'o11y/metrics.html',
        {'scope_metrics': ScopeMetrics.objects.all()}
    )

def traces(req):
    spans = ScopeSpans.objects.all()
    return render(
        req,
        'o11y/traces.html',
        {'scope_spans': spans}
    )

def fastapi(req):
    return handle_request(req, '8001')

def flask(req):
    return handle_request(req, '8002')

def bottle(req):
    return handle_request(req, '8003')

def pyramid(req):
    return handle_request(req, '8004')

def tornado(req):
    return handle_request(req, '8005')

def handle_request(req, port):
    client_lib = req.GET.get('client_lib')
    path = 'http://localhost:' + port
    if client_lib == 'urllib':
        with urllib.request.urlopen(path) as resp:
            return JsonResponse(json.loads(resp.read()))
    elif client_lib == 'httpx':
        return JsonResponse(httpx.get(path).json())
    elif client_lib == 'requests':
        resp = requests.get(path)
        return JsonResponse(json.loads(resp.text))
