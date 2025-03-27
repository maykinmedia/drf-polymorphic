DRF-polymorphic
===============

:Version: 2.0.0
:Source: https://github.com/maykinmedia/drf-polymorphic
:Keywords: django, rest, polymorphic

|build-status| |coverage| |linting| |black| |docs|

|python-versions| |django-versions| |pypi-version|

Polymorphic support for DRF without Django models

Overview
========

Polymorphism happens when a resource takes a certain shape depending on the type
of the resource. Usually they have a common base type. The exact type/shape is not
statically known, but depends on the run-time values.

Unlike `django-rest-polymorphic <https://github.com/apirobot/django-rest-polymorphic>`_
this implementation doesn't require the usage of ``django-polymorphic`` model classes
and can be used even without django models.

The implementations also includes the extension for `DRF spectacular`_ schema generation.

See the documentation_ for getting started and usage examples.


.. |build-status| image:: https://github.com/maykinmedia/drf-polymorphic/workflows/ci/badge.svg
    :target: https://github.com/maykinmedia/drf-polymorphic/actions/workflows/ci.yml
    :alt: Run CI

.. |linting| image:: https://github.com/maykinmedia/drf-polymorphic/workflows/code-quality/badge.svg
    :target: https://github.com/maykinmedia/drf-polymorphic/actions/workflows/code-quality.yml
    :alt: Code linting

.. |coverage| image:: https://codecov.io/gh/maykinmedia/drf-polymorphic/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/drf-polymorphic
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/drf-polymorphic.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/drf-polymorphic.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-polymorphic.svg
    :target: https://pypi.org/project/drf-polymorphic/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |docs| image:: https://readthedocs.org/projects/drf-polymorphic/badge/?version=latest
    :target: https://drf-polymorphic.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. _DRF spectacular: https://drf-spectacular.readthedocs.io/en/latest/

.. _documentation: https://drf-polymorphic.readthedocs.io/
