from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
]
