from django.core.exceptions import ImproperlyConfigured

import pytest
from hypothesis import given, strategies as st
from rest_framework import serializers

from drf_polymorphic.serializers import PolymorphicSerializer


def test_no_mapping_specified():
    class Serializer(PolymorphicSerializer):
        pass

    with pytest.raises(ImproperlyConfigured):
        Serializer()


@given(
    st.one_of(
        st.integers(),
        st.floats(),
        st.binary(),
        st.booleans(),
    )
)
def test_invalid_discriminator_type(t):
    class Serializer(PolymorphicSerializer):
        serializer_mapping = {}
        discriminator_field = t

    with pytest.raises(ImproperlyConfigured):
        Serializer()


class ChildSerializer(serializers.Serializer):
    some_text = serializers.CharField()


def test_serializer_mapping_can_take_instances_and_classes():
    class Serializer(PolymorphicSerializer):
        object_type = serializers.ChoiceField(choices=["class", "instance"])

        serializer_mapping = {
            "class": ChildSerializer,
            "instance": ChildSerializer(),
        }

    data = [
        {"object_type": "class", "some_text": "a text"},
        {"object_type": "instance", "some_text": "another text"},
    ]

    serializer = Serializer(instance=data, many=True)

    assert serializer.data == data
