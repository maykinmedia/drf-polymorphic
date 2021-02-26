from django.contrib import admin
from django.urls import path

from .views import PetView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pets/", PetView.as_view(), name="pets"),
]
