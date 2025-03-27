import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from testapp.data import Cat, Pet, pets
from testapp.serializers import PetPolymorphicSerializer


def test_get_pets(api_client):
    url = reverse("pets")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = [
        {"name": "Snowball", "pet_type": "cat", "hunting_skill": "lazy"},
        {"name": "Lady", "pet_type": "dog", "bark": "soft"},
        {"name": "John", "pet_type": "lizard", "loves_rocks": True},
    ]

    assert response.json() == expected_data


def test_create_pet(api_client):
    url = reverse("pets")
    data = {"name": "Felix", "pet_type": "cat", "hunting_skill": "active"}

    assert len(pets) == 3

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert len(pets) == 4

    new_pet = pets[-1]

    assert isinstance(new_pet, Cat) is True
    assert new_pet.name == "Felix"
    assert new_pet.hunting_skill == "active"


def test_with_just_base_type_errors_strict_mode():
    data = [
        Pet(name="No Type"),
        Cat(name="Ziggy", hunting_skill="bird obsession"),
    ]
    serializer = PetPolymorphicSerializer(instance=data, many=True)

    with pytest.raises(KeyError):
        serializer.data


def test_with_just_base_type_no_errors_non_strict_mode():
    data = [
        Pet(name="No Type"),
        Cat(name="Ziggy", hunting_skill="bird obsession"),
    ]

    class NonStrictSerializer(PetPolymorphicSerializer):
        strict = False

    serializer = NonStrictSerializer(instance=data, many=True)

    assert serializer.data == [
        {
            "name": "No Type",
            "pet_type": "",
        },
        {
            "name": "Ziggy",
            "hunting_skill": "bird obsession",
            "pet_type": "cat",
        },
    ]


def test_validate_nullable():
    serializer = PetPolymorphicSerializer(required=False, allow_null=True, data=None)

    valid = serializer.is_valid()

    assert valid
