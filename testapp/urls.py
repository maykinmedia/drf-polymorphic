from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularJSONAPIView

from .views import PetView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path(
                    "", SpectacularJSONAPIView.as_view(schema=None), name="schema-json"
                ),
                path("pets/", PetView.as_view(), name="pets"),
            ]
        ),
    ),
]
