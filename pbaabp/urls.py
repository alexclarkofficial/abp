from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("pages.urls")),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", include("profiles.urls")),
    path("events/", include("events.urls")),
    path("donations/", include("membership.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path("admin/", admin.site.urls),
]
