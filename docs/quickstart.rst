==========
Quickstart
==========

Installation
============

Install using pip:

.. code-block:: bash

    pip install drf-polymorphic

Then add ``drf_polymorphic`` to installed apps in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "drf_polymorphic",
        ...
    ]

Usage
=====

For example, you have data for pets where the structure depends on the pet species:

.. code-block:: python

    from dataclasses import dataclass


    @dataclass
    class Pet:
        name: str
        pet_type = ""


    @dataclass
    class Cat(Pet):
        hunting_skill: str
        pet_type = "cat"


    @dataclass
    class Dog(Pet):
        bark: str
        pet_type = "dog"


    @dataclass
    class Lizard(Pet):
        loves_rocks: bool
        pet_type = "lizard"


    cat = Cat(name="Snowball", hunting_skill="lazy")
    dog = Dog(name="Lady", bark="soft")
    lizard = Lizard(name="John", loves_rocks=True)

    pets = [cat, dog, lizard]

You can use ``drf-polymorphic`` to show all this data in one endpoint.
Define regular serializers for each ``pet_type``:

.. code-block:: python

    # serializers.py
    from rest_framework import serializers


    class CatSerializer(serializers.Serializer):
        hunting_skill = serializers.ChoiceField(
            choices=[("lazy", "lazy"), ("active", "active")]
        )


    class DogSerializer(serializers.Serializer):
        bark = serializers.ChoiceField(choices=[("soft", "soft"), ("loud", "loud")])


    class LizardSerializer(serializers.Serializer):
        loves_rocks = serializers.BooleanField()


Now a polymorphic serializer can be created, which maps the values of ``pet_type`` with the
serializers defined above:

.. code-block:: python

    # serializers.py
    from drf_polymorphic.serializers import PolymorphicSerializer


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

Create ``APIView`` which uses this polymorphic serializer:

.. code-block:: python

    from rest_framework.response import Response
    from rest_framework.views import APIView

    from .serializers import PetPolymorphicSerializer


    class PetView(APIView):
        serializer_class = PetPolymorphicSerializer

        def get(self, request, *args, **kwargs):
            serializer = self.serializer_class(pets, many=True)
            return Response(serializer.data)

        def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


After the path is added to ``urls.py`` the endpoint is ready to use.

Let's display all the pets with GET request:

.. code-block:: http

    GET /pets/ HTTP/1.1

    HTTP/1.0 200 OK
    Content-Type: application/json
    [
        {
            "name": "Snowball",
            "pet_type": "cat",
            "hunting_skill": "lazy"
        },
        {
            "name": "Lady",
            "pet_type": "dog",
            "bark": "soft"
        },
        {
            "name": "John",
            "pet_type": "lizard",
            "loves_rocks": true
        }
    ]


The same endpoint can be used to change the data. In this example the request body can
include data of any predefined pet species:

.. code-block:: http

    POST /pets/ HTTP/1.1
    {
        "name": "Felix",
        "pet_type": "cat",
        "hunting_skill": "active"
    }

    HTTP/1.0 201 Created
    {
        "name": "Felix",
        "pet_type": "cat",
        "hunting_skill": "active"
    }

Now the ``pets`` list will include one more pet, which is the instance of ``Cat`` class.
