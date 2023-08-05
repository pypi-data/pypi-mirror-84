""" URL definitions for the application. Used for testing purposes only. """

from django.urls import path, include

from . import views

urlpatterns = [
    path("auth/", include("mozilla_django_oidc.urls")),
    path("", views.TestView.as_view(), name="selfauth-test"),
]
