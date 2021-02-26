from rest_framework import serializers

from drf_polymorphic.serializers import PolymorphicSerializer


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
