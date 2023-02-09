.. drf-polymorphic documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============
DRF-polymorphic
===============

|build-status| |coverage| |linting|

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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |build-status| image:: https://travis-ci.org/maykinmedia/drf-polymorphic.svg?branch=master
    :target: https://travis-ci.org/maykinmedia/drf-polymorphic

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/drf-polymorphic/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/drf-polymorphic
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/drf-polymorphic.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/drf-polymorphic.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/drf-polymorphic.svg
    :target: https://pypi.org/project/drf-polymorphic/
