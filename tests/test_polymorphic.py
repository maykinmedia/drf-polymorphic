from rest_framework import status
from rest_framework.reverse import reverse


def test_get_pets(api_client):
    url = reverse("pets")

    response = api_client.get(url)

    assert response.status == status.HTTP_200_OK

    expected_data = [
        {"name": "Snowball", "pet_type": "cat", "hunting_skill": "lazy"},
        {"name": "Lady", "pet_type": "dog", "bark": "soft"},
        {"name": "John", "pet_type": "lizard", "loves_rocks": True},
    ]

    assert response.json() == expected_data
