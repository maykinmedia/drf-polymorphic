from django.apps import AppConfig


class DrfPolymorphicConfig(AppConfig):
    name = "drf_polymorphic"

    def ready(self):
        from .extensions import PolymorphicSerializerExtension  # noqa
