from rest_framework import serializers, status, views
from rest_framework.reverse import reverse

from drf_polymorphic.serializers import PolymorphicSerializer

from . import assert_schema
from .schema import generate_schema


def test_get_schema(api_client):
    url = reverse("schema")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_schema = response.content.decode()

    assert_schema(response_schema, "schema.yaml")


def test_polymorphic_extension_component_names():
    class Dummy(PolymorphicSerializer):
        object_type = serializers.ChoiceField(choices=["foo", "bar"])
        serializer_mapping = {}

    class XView(views.APIView):
        serializer_class = Dummy

        def get(self, *args, **kwargs): ...

    schema = generate_schema("x", view=XView)

    assert "Dummy" in schema["components"]["schemas"]
    assert schema["components"]["schemas"]["Dummy"] == {
        "oneOf": [],
        "discriminator": {"propertyName": "object_type", "mapping": {}},
    }


def test_polymorphic_extension_alternative_discriminator():
    class DummySerializer(PolymorphicSerializer):
        type = serializers.ChoiceField(choices=["foo", "bar"])
        serializer_mapping = {}
        discriminator_field = "type"

    class XView(views.APIView):
        serializer_class = DummySerializer

        def get(self, *args, **kwargs): ...

    schema = generate_schema("x", view=XView)

    assert "Dummy" in schema["components"]["schemas"]
    assert schema["components"]["schemas"]["Dummy"] == {
        "oneOf": [],
        "discriminator": {"propertyName": "type", "mapping": {}},
    }


def test_polymorphic_extension_generic_subserializer(no_warnings):
    class Nested(serializers.Serializer):
        pass

    class DummySerializer(PolymorphicSerializer):
        object_type = serializers.ChoiceField(choices=["foo", "bar"])
        # note this raises a warning and it's better to use None instead or provide an
        # explicit subclasses serializer with a proper name
        serializer_mapping = {"foo": Nested}

    class XView(views.APIView):
        serializer_class = DummySerializer

        def get(self, *args, **kwargs): ...

    schema = generate_schema("x", view=XView)

    schemas = schema["components"]["schemas"]
    assert "Dummy" in schemas
    assert "GenericObject" in schemas

    assert schemas["GenericObject"] == {
        "type": "object",
        "description": "Generic object",
        "additionalProperties": True,
    }


def test_multiple_occurences_of_same_combined_serializer():
    class Nested(serializers.Serializer):
        name = serializers.CharField()

    class DummySerializer(PolymorphicSerializer):
        object_type = serializers.ChoiceField(choices=["foo", "bar"])
        serializer_mapping = {"foo": Nested, "bar": Nested}

    class XView(views.APIView):
        serializer_class = DummySerializer

        def get(self, *args, **kwargs): ...

    schema = generate_schema("x", view=XView)

    schemas = schema["components"]["schemas"]
    assert "Dummy" in schemas
    assert len(schemas["Dummy"]["oneOf"]) == 1
