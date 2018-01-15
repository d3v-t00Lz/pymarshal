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
        desc: Contains the URIs for this service
        args:
            -   name: routes
                type: list
                subtypes: [Route]
                desc: a mapping of URIs to Route instances
                ctor: pymarshal.api_docs.routes.Route.__init__
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
        desc: Describes a URI and it's HTTP methods
        args:
            -   name: module
                type: str
                desc: The name of the module to load the handlers from
            -   name: methods
                type: list
                subtypes: ["RouteMethod"]
                desc: The HTTP request methods to use
                ctor: pymarshal.api_docs.routes.RouteMethod.__init__
            -   name: uri
                type: str
                desc: The path of this route
            -   name: hide
                type: bool
                desc: True to hide from the API docs, otherwise False
                required: false
                default: false
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
    _marshal_exclude = [
        'method_choices',
    ]
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
        desc: Describes a single HTTP method of a URI
        args:
            -   name: method
                type: str
                desc: The HTTP request method to use
            -   name: description
                type: str
                desc: The description of what this call does
                required: false
                default: ""
            -   name: request_example
                type: dict
                desc: An example JSON request body
                required: false
                default: null
            -   name: request_help
                type: DocString
                desc: Help for @request_example
                required: false
                default: null
            -   name: response_example
                type: dict
                desc: An example JSON response body
                required: false
                default: null
            -   name: response_help
                type: DocString
                desc: Help for @response_example
                required: false
                default: null
            -   name: method_choices
                type: list
                subtypes: ["str"]
                desc: The HTTP methods to allow for @method
                hide: true
                required: false
                default: [DELETE, GET, PATCH, POST, PUT]
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
        desc: Describes a single HTTP method of a URI
        args:
            -   name: method
                type: str
                desc: The HTTP request method to use
            -   name: description
                type: str
                desc: The description of what this call does
                required: false
                default: ""
            -   name: request_example
                type: dict
                desc: An example JSON request body
                required: false
                default: null
            -   name: request_ctor
                type: method
                desc: Docstring will be parsed into help for @request_example
                required: false
                default: null
            -   name: response_example
                type: dict-or-None
                desc: An example JSON response body
                required: false
                default: null
            -   name: response_ctor
                type: method
                desc: Help for @response_example
                required: false
                default: null
            -   name: method_choices
                type: list
                subtypes: ["str"]
                desc: The HTTP methods to allow for @method
                hide: true
                required: false
                default: [DELETE, GET, PATCH, POST, PUT]
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
