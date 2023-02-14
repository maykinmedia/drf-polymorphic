from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularYAMLAPIView

from .views import PetView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path(
                    "", SpectacularYAMLAPIView.as_view(schema=None), name="schema"
                ),  # type:ignore
                path("pets/", PetView.as_view(), name="pets"),  # type:ignore
            ]
        ),
    ),
]
