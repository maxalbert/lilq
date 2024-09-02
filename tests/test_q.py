from collections import namedtuple

from lilq import Q, If

from unittest.mock import Mock

Item = namedtuple("Item", ["aaa", "bbb"])


def test_simple_query():
    q = Q(aaa="foo")
    item1 = Mock(aaa="foo")
    item2 = Mock(aaa="quux")
    assert q.matches(item1)
    assert not q.matches(item2)


def test_simple_transformation():
    q = If(aaa="foo").then(aaa="bar", bbb="quux")
    item1 = Item(aaa="foo", bbb=None)
    item2 = Item(aaa="lol", bbb=None)

    item1_new = q.apply(item1)
    item2_new = q.apply(item2)

    assert item1_new.aaa == "bar"
    assert item1_new.bbb == "quux"
    assert item2_new.aaa == "lol"
    assert item2_new.bbb is None
