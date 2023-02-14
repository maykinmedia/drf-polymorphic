"""
Code taken from drf-spectacular,
https://github.com/tfranzel/drf-spectacular/blob/24b8a9890d59900d102490a48e286d08cdcc7ab5/tests/__init__.py#L64

Copyright © 2011-present, Encode OSS Ltd.
Copyright © 2019-present, T. Franzel <tfranzel@gmail.com>, Cashlink Technologies GmbH.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from drf_spectacular.validation import validate_schema


def generate_schema(route, viewset=None, view=None, view_function=None, patterns=None):
    from django.urls import path

    from drf_spectacular.generators import SchemaGenerator
    from rest_framework import routers
    from rest_framework.viewsets import ViewSetMixin

    if viewset:
        assert issubclass(viewset, ViewSetMixin)
        router = routers.SimpleRouter()
        router.register(route, viewset, basename=route)
        patterns = router.urls
    elif view:
        patterns = [path(route, view.as_view())]
    elif view_function:
        patterns = [path(route, view_function)]
    else:
        assert route is None and isinstance(patterns, list)

    generator = SchemaGenerator(patterns=patterns)
    schema = generator.get_schema(request=None, public=True)
    validate_schema(schema)  # make sure generated schemas are always valid
    return schema
