"""

"""

import pytest

from pymarshal.api_docs.routes import *


def test_routes_dups():
    with pytest.raises(ValueError):
        Routes(
            routes=[
                Route(
                    module='',
                    methods=[
                        RouteMethod.factory('GET'),
                    ],
                    uri='/api/v1/testing',
                ),
                Route(
                    module='',
                    methods=[],
                    uri='/api/v1/testing',
                ),
            ]
        )


def test_route_method_eq():
    assert RouteMethod('GET') == RouteMethod('GET')


def test_route_method_hash():
    hash(RouteMethod('GET'))
