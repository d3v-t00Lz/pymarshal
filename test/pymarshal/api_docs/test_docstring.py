"""

"""

from pymarshal.api_docs.docstring import (
    DocStringArg,
    DocStringRaise,
    DocStringReturn,
)


class DocA:
    def __init__(
        self,
        b,
        c=5,
    ):
        """
        desc: testing
        args:
            -   name: b
                type: int
                desc: blah
            -   name: c
                type: int
                desc: blah
                required: false
                default: 5
        """
        self.b = b


def test_docstringarg_recursive():
    ctor = '.'.join([
        __name__,
        DocA.__name__,
        '__init__',
    ])
    d = DocStringArg.factory(
        'test',
        'test',
        'test',
        ctor=ctor,
    )
    assert d.docstring


def test_docstringraise():
    # should not raise
    DocStringRaise(
        '',
        '',
    )


def test_docstringreturn():
    # should not raise
    DocStringReturn(
        '',
        '',
    )
