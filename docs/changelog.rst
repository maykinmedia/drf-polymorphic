=========
Changelog
=========

2.1.1 (2025-07-15)
==================

Schema generation bugfix release.

* Fixed splitting patch schema generation when ``COMPONENT_SPLIT_PATCH`` is enabled.
* Fixed warning during schema generation for duplicated registrations of component
  schemas.

2.1.0 (2025-07-04)
==================

Small feature release.

* Confirmed Django 5.2 support.
* You can now map to ``None`` if the value of the discriminator does not require
  additional fields.
* You can now use ``models.TextChoices`` values as keys in the ``serializer_mapping``.
* The discriminator field name is now properly camelized in the drf-spectacular generated
  schema if the matching post-processing hook is enabled for projects that use
  djangorestframework-camel-case.

2.0.1 (2025-07-03)
==================

Bugfix release.

* Identified and fixed crash during validation when the discriminator field has a
  default and is omitted from the initial data.

2.0.0 (2025-03-27)
==================

Maintenance and bugfix release.

**💥 Breaking changes**

* Dropped support for Python 3.8 and 3.9.
* Dropped support for Django 3.2 and 4.1.

**Features**

* Support for Python 3.12 is confirmed.

**Bugfixes**

* Fixed a crash during validation when the polymorphic serializer allows ``None`` values
  or is not required.


1.0.0 (2023-02-14)
==================

Published stable version.

See the docs for usage.

0.1.0 (2023-02-14)
==================

Published initial version to PyPI.
