"""

"""

import inspect

from pymarshal.json import *
from pymarshal.util.checks import check_dups
from pymarshal.util.init_args import init_args

from .docstring import DocString

__all__ = [
    'init_args',
    'inspect',
    'marshal_json',
    'Route',
    'RouteMethod',
    'Routes',
]


# The methods applicable to RESTful services
HTTP_METHODS = (
    'DELETE',
    'GET',
    'HEAD',
    'PATCH',
    'POST',
    'PUT',
)


class Routes:
    def __init__(
        self,
        routes,
    ):
        """
        Args:
            routes: dict[str]=Route, a mapping of URIs to Route instances
        """
        self.routes = type_assert_iter(
            routes,
            Route,
        )
        check_dups(routes)



class Route:
    def __init__(
        self,
        module,
        methods,
        uri,
        hide=False,
    ):
        """
        Args:
            module:  str, The name of the module to load the handlers from
            methods: list-of-RouteMethod, the HTTP request methods to use
            uri:     str, The path of this route
            hide:    bool, True to hide from the API docs, otherwise False
        """
        self.module = type_assert(module, str)
        self.methods = type_assert_iter(
            methods,
            RouteMethod,
        )
        check_dups(methods)
        self.uri = type_assert(uri, str)
        self.hide = type_assert(hide, bool)

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, other):
        return self.uri == other.uri


class RouteMethod:
    def __init__(
        self,
        method,
        description="",
        request_example=None,
        request_help=None,
        response_example=None,
        response_help=None,
        method_choices=HTTP_METHODS,
    ):
        """
        Args:
            method:           str, The HTTP request method to use
            description:      str, The description of what this call does
            request_example:  dict-or-None, An example JSON request body
            request_help:     DocString-or-None, Help for @request_example
            response_example: dict-or-None, An example JSON response body
            response_help:    DocString-or-None, Help for @response_example
        """
        self.method = type_assert(
            method,
            str,
            choices=method_choices,
        )
        self.description = type_assert(description, str)
        self.request_example = type_assert(
            request_example,
            (dict, list),
            allow_none=True,
        )
        self.request_help = type_assert(
            request_help,
            DocString,
            allow_none=True,
        )
        self.response_example = type_assert(
            response_example,
            (dict, list),
            allow_none=True,
        )
        self.response_help = type_assert(
            response_help,
            DocString,
            allow_none=True,
        )

    @staticmethod
    def factory(
        method,
        description="",
        request_example=None,
        request_ctor=None,
        response_example=None,
        response_ctor=None,
        method_choices=HTTP_METHODS,
    ):
        """
        Args:
            method:           str, The HTTP request method to use
            description:      str, The description of what this call does
            request_example:  dict-or-None, An example JSON request body
            request_ctor:     function-or-method, The constructor of the
                              class the request body will be unmarshalled
                              into.
            response_example: dict-or-None, An example JSON request body
            response_ctor:    function-or-method, The constructor of the
                              class the response body will be marshalled
                              into.
        """
        return RouteMethod(
            method,
            description,
            request_example,
            DocString.from_ctor(request_ctor) if request_ctor else None,
            response_example,
            DocString.from_ctor(response_ctor) if response_ctor else None,
            method_choices,
        )

    def __hash__(self):
        return hash(self.method)

    def __eq__(self, other):
        return self.method == other.method
