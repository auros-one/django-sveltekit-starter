from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from django.urls import path

urlpatterns = [
    path("", SpectacularRedocView.as_view(url_name="schema"), name="docs"),
    path("schema", SpectacularAPIView.as_view(), name="schema"),
]
