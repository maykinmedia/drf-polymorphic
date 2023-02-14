from django.apps import AppConfig, apps


class DrfPolymorphicConfig(AppConfig):
    name = "drf_polymorphic"

    def ready(self):
        if apps.is_installed("drf_spectacular"):  # pragma: no cover
            from . import extensions  # noqa
