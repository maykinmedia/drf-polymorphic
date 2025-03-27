from typing import Dict, Optional, Type, Union

from django.core.exceptions import ImproperlyConfigured

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.utils.serializer_helpers import ReturnDict

SerializerCls = Type[serializers.Serializer]
SerializerClsOrInstance = Union[serializers.Serializer, SerializerCls]


class PolymorphicSerializer(serializers.Serializer):
    """
    Polymorphic serializer base class.

    Note that the discriminator field must exist at the same depth as the mapped
    serializer fields for the OpenAPI introspection. See
    https://swagger.io/docs/specification/data-models/inheritance-and-polymorphism/ for
    more information. As such, it's not possible to define something like:

    {
        "object_type": "foo",
        "polymorphic_context": {
            <foo-specific fields>
        }
    }

    without explicitly wrapping this in a parent serializer, i.e. -
    ``polymorphic_context`` can not be a PolymorphicSerializer itself, as it requires
    access to the ``object_type`` in the parent scope.
    """

    # mapping of discriminator value to serializer (instance or class)
    serializer_mapping: Dict[str, SerializerClsOrInstance]
    _serializer_mapping: Dict[str, serializers.Serializer]

    # the serializer field that holds the discriminator values
    discriminator_field: str = "object_type"
    strict = True

    # drf-typehints missing in pyright
    _errors: ReturnDict

    def __new__(cls, *args, **kwargs):
        if (mapping := getattr(cls, "serializer_mapping", None)) is None:
            raise ImproperlyConfigured(
                "`{cls}` is missing a `{cls}.serializer_mapping` attribute".format(
                    cls=cls.__name__
                )
            )

        if not isinstance(cls.discriminator_field, str):
            raise ImproperlyConfigured(
                "`{cls}.discriminator_field` must be a string".format(cls=cls.__name__)
            )

        instance = super().__new__(cls, *args, **kwargs)

        # normalize the serializer mapping
        instance._serializer_mapping = {}
        for obj_type, serializer_or_cls in mapping.items():
            if isinstance(serializer_or_cls, serializers.Serializer):
                serializer = serializer_or_cls
            else:
                serializer = serializer_or_cls(*args, **kwargs)
                serializer.parent = instance
            instance._serializer_mapping[obj_type] = serializer

        return instance

    @property
    def discriminator(self) -> serializers.Field:
        return self.fields[self.discriminator_field]

    def to_representation(self, instance):
        default = super().to_representation(instance)
        serializer = self._get_serializer_from_instance(instance)
        extra = serializer.to_representation(instance) if serializer is not None else {}
        return {**default, **extra}

    def to_internal_value(self, data):
        default = super().to_internal_value(data)
        serializer = self._get_serializer_from_data(data)
        if serializer is None:
            return default
        extra = serializer.to_internal_value(data)
        return {**default, **extra}

    def is_valid(self, *args, **kwargs):
        valid = super().is_valid(*args, **kwargs)
        if self.validated_data is None:
            return valid
        extra_serializer = self._get_serializer_from_data(self.validated_data)
        if extra_serializer is None:
            return valid
        extra_valid = extra_serializer.is_valid(*args, **kwargs)
        self._errors.update(extra_serializer.errors)
        return valid and extra_valid

    def run_validation(self, data=empty):
        (is_empty_value, data) = self.validate_empty_values(data)
        if is_empty_value:
            return data

        value = super().run_validation(data=data)
        extra_serializer = self._get_serializer_from_data(data)
        validated_data = (
            extra_serializer.run_validation(data) if extra_serializer else {}
        )
        return {**value, **validated_data}

    def _discriminator_serializer(
        self, discriminator_value: str
    ) -> Optional[serializers.Serializer]:
        try:
            return self._serializer_mapping[discriminator_value]
        except KeyError as exc:
            if self.strict:
                raise KeyError(
                    "`{cls}.serializer_mapping` is missing a corresponding serializer "
                    "for the `{value}` key".format(
                        cls=self.__class__.__name__,
                        value=discriminator_value,
                    )
                ) from exc
            return None

    def _get_serializer_from_data(self, data):
        discriminator_value = self.discriminator.get_value(data)
        serializer = self._discriminator_serializer(discriminator_value)
        return serializer

    def _get_serializer_from_instance(self, instance):
        discriminator_value = self.discriminator.get_attribute(instance)
        assert isinstance(
            discriminator_value, str
        ), "OpenAPI spec only allows strings as mapping keys"
        serializer = self._discriminator_serializer(discriminator_value)
        return serializer
