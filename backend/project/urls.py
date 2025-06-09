from django.urls import include, path, re_path

from project.accounts.admin import admin_site  # Import custom admin site
from project.core.views import AuthCheck, FlowerProxyView, HealthCheck

urlpatterns = [
    path("api/__debug__/", include("debug_toolbar.urls")),
    re_path(
        r"^api/admin/flower/(?P<path>.*)",
        FlowerProxyView.as_view(),
    ),
    path("api/admin/", admin_site.urls),  # Use custom admin site
    path("api/docs/", include("project.core.docs.urls")),
    path("api/accounts/", include("project.accounts.urls")),
    path("api/healthcheck/", HealthCheck.as_view(), name="healthcheck"),
    path("api/authcheck/", AuthCheck.as_view(), name="authcheck"),
]
