from django.utils.module_loading import import_string

from rest_framework import serializers

from drf_polymorphic.serializers import PolymorphicSerializer

from .data import pets


class CatSerializer(serializers.Serializer):
    hunting_skill = serializers.ChoiceField(
        choices=[("lazy", "lazy"), ("active", "active")]
    )


class DogSerializer(serializers.Serializer):
    bark = serializers.ChoiceField(choices=[("soft", "soft"), ("loud", "loud")])


class LizardSerializer(serializers.Serializer):
    loves_rocks = serializers.BooleanField()


class PetPolymorphicSerializer(PolymorphicSerializer):
    name = serializers.CharField()
    pet_type = serializers.ChoiceField(
        choices=[("cat", "cat"), ("dog", "dog"), ("lizard", "lizard")]
    )

    discriminator_field = "pet_type"
    serializer_mapping = {
        "cat": CatSerializer,
        "dog": DogSerializer,
        "lizard": LizardSerializer,
    }

    def create(self, validated_data):
        pet_type = validated_data.pop("pet_type")
        pet_class = import_string(f"testapp.data.{pet_type.capitalize()}")
        new_pet = pet_class(**validated_data)
        pets.append(new_pet)

        return new_pet
