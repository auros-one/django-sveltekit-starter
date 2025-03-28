from django.contrib import admin
from django.urls import include, path, re_path

from project.core.views import AuthCheck, FlowerProxyView, HealthCheck

urlpatterns = [
    path("api/__debug__/", include("debug_toolbar.urls")),
    re_path(
        r"^api/admin/flower/(?P<path>.*)",
        FlowerProxyView.as_view(),
    ),
    path("api/admin/", admin.site.urls),
    path("api/docs/", include("project.core.docs.urls")),
    path("api/accounts/", include("project.accounts.urls")),
    path("api/healthcheck/", HealthCheck.as_view(), name="healthcheck"),
    path("api/authcheck/", AuthCheck.as_view(), name="authcheck"),
]
