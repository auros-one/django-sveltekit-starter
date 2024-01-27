from django.contrib import admin
from django.urls import include, path
from project.utils.views import AuthCheck, HealthCheck

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
    path("docs/", include("project.docs.urls")),
    path("accounts/", include("project.accounts.urls")),
    path("healthcheck/", HealthCheck.as_view(), name="healthcheck"),
    path("authcheck/", AuthCheck.as_view(), name="private-healthcheck"),
]
