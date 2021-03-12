from rest_framework import status
from rest_framework.reverse import reverse

from testapp.data import Cat, pets
from tests import assert_schema


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


def test_get_schema(api_client):
    url = reverse("schema")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    response_schema = response.content.decode()

    assert_schema(response_schema, "schema.yaml")
