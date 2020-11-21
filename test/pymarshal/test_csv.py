from pymarshal.csv import *

def test_marshal_unmarshal():
    class Test:
        def __init__(self, a, b):
            self.a = a
            self.b = b

    u = [Test("a", 2), Test("b", 3)]
    assert u[0].a == "a", u[0].a
    m = marshal_csv(u, Test)
    assert m[0][0] == "a", m[0][0]
    u = unmarshal_csv(m, Test)
    assert u[0].a == "a", u[0].a

