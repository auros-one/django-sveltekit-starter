from django.urls import include, path

urlpatterns = [
    path("accounts/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/signup/", include("dj_rest_auth.registration.urls")),
]
