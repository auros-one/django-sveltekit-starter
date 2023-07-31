from django.urls import include, path

urlpatterns = [
    path("signup/", include("dj_rest_auth.registration.urls"), name="signup"),
    path("", include("dj_rest_auth.urls")),
]
