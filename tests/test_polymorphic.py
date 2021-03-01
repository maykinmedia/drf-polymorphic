from rest_framework import status
from rest_framework.reverse import reverse


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


def test_get_schema(api_client):
    url = reverse("schema-json")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    schema = response.json()
    pet_schema = schema["components"]["schemas"]["PetPolymorphic"]

    assert "discriminator" in pet_schema
    assert pet_schema["discriminator"]["propertyName"] == "pet_type"
