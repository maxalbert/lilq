from lilq import Q, If

from unittest.mock import Mock


def test_simple_query():
    q = Q(foo="bar")
    item1 = Mock(foo="bar")
    item2 = Mock(foo="quux")
    assert q.matches(item1)
    assert not q.matches(item2)


def test_simple_transformation():
    q = If(aaa="foo").then(aaa="bar", bbb="quux")
    item1 = Mock(aaa="foo")
    item2 = Mock(aaa="lol")

    q.apply(item1)
    q.apply(item2)

    assert item1.aaa == "bar"
    assert item1.bbb == "quux"
    assert item2.aaa == "lol"
    assert not hasattr(item2, "bbb") or item2.bbb != "quux"
