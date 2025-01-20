from django.contrib import admin
from django.urls import include, path

from project.core.views import AuthCheck, HealthCheck

urlpatterns = [
    path("api/__debug__/", include("debug_toolbar.urls")),
    path("api/admin/", admin.site.urls),
    path("api/docs/", include("project.core.docs.urls")),
    path("api/accounts/", include("project.accounts.urls")),
    path("api/healthcheck/", HealthCheck.as_view(), name="healthcheck"),
    path("api/authcheck/", AuthCheck.as_view(), name="authcheck"),
]
