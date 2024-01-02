from django.urls import path

from o11y import views

urlpatterns = [
    path("", views.index, name="index"),
    path("metrics/", views.metrics, name="metrics"),
    path("fastapi/", views.fastapi, name="fastapi"),
    path("flask/", views.flask, name="flask"),
    path("bottle/", views.bottle, name="bottle"),
    path("pyramid/", views.pyramid, name="pyramid"),
    path("tornado/", views.tornado, name="tornado"),
]
