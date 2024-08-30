from lilq import Q

from unittest.mock import Mock


def test_simple_query():
    q = Q(foo="bar")
    item1 = Mock(foo="bar")
    item2 = Mock(foo="quux")
    assert q.matches(item1)
    assert not q.matches(item2)
