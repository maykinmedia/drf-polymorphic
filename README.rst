drf_polymorphic
===============

:Version: 0.1.0
:Source: https://github.com/maykinmedia/drf_polymorphic
:Keywords: django, rest, polymorphic
:PythonVersion: 3.7, 3.8

|build-status| |coverage| |linting|

Polymorphic support for DRF without Django models

Overview
========

Polymorphism happens when a resource takes a certain shape depending on the type
of the resource. Usually they have a common base type. The exact type/shape is not
statically known, but depends on the run-time values.

Unlike `django-rest-polymorphic <https://github.com/apirobot/django-rest-polymorphic>`_
this implementation doesn't require the usage of ``django-polymorphic`` Model
and can be used even without django models.

The implementations also includes the extension for ``drf_spectacular`` schema generation.

``drf_polymorphic`` is inspired on the vng-api-common `implementation
<https://github.com/VNG-Realisatie/vng-api-common/blob/master/vng_api_common/polymorphism.py>`_

Installation
============
Install using pip:

.. code-block:: bash

    pip install drf_polymorphic

Then add ``drf_polymorphic`` to installed apps in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        # ALL YOUR APPS
        'drf_polymorphic',
    ]


Usage
=====

For example, you have data for pets with structure dependent on the type of the pet:

.. code-block:: python

    from dataclasses import dataclass


    @dataclass
    class Pet:
        name: str


    @dataclass
    class Cat(Pet):
        hunting_skill: str
        pet_type: str = 'cat'


    @dataclass
    class Dog(Pet):
        bark: str
        pet_type: str = 'dog'


    @dataclass
    class Lizard(Pet):
        loves_rocks: bool
        pet_type: str = 'lizard'


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


    class PetPolymorphicSerializer(PolymorphicSerializer):
        name = serializers.CharField()
        pet_type = serializers.ChoiceField(
            choices=[("cat", "cat"), ("dog", "dog"), ("lizard", "lizard")]
        )

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

After a path is added to ``urls.py`` the endpoint is ready to use:

.. code-block:: bash

    $ http GET "http://localhost:8000/pets/"

.. code-block:: http

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


DRF spectacular support
=======================

``drf_polymorphic`` includes an extension for `drf_spectacular <https://drf-spectacular.readthedocs.io/en/latest/>`_
schema generation. If you use ``drf_spectacular`` in your project this extension will be
loaded automatically.


.. |build-status| image:: https://github.com/maykinmedia/drf-polymorphic/workflows/ci/badge.svg
    :target: https://github.com/maykinmedia/drf-polymorphic/actions/workflows/ci.yml
    :alt: Run CI

.. |linting| image:: https://github.com/maykinmedia/drf-polymorphic/workflows/code-quality/badge.svg
    :target: https://github.com/maykinmedia/drf-polymorphic/actions/workflows/code-quality.yml
    :alt: Code linting

.. |coverage| image:: https://codecov.io/gh/maykinmedia/drf-polymorphic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/drf-polymorphic
    :alt: Coverage status
