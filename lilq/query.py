from abc import ABCMeta, abstractmethod
from typing import Any

from.transformation import Transformation


class BaseQuery(metaclass=ABCMeta):
    def bind(self, target: Any):
        return BoundQuery(self, target=target)

    @abstractmethod
    def matches(self, target: Any):
        raise NotImplementedError()


class BoundQuery:
    def __init__(self, query: BaseQuery, target: Any):
        self.query = query
        self.target = target

    def __bool__(self):
        return self.query.matches(self.target)


def get_matcher_func(key: str, value: str):
    if key.endswith("__startswith"):
        def _func(target):
            attr_name = key.removesuffix("__startswith")
            return getattr(target, attr_name).startswith(value)
    else:
        def _func(target):
            return getattr(target, key) == value
    return _func

class Q(BaseQuery):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.matchers = [get_matcher_func(key, value) for (key, value) in self.kwargs.items()]

    def __repr__(self):
        clsname = self.__class__.__name__
        arg_strings = [f"{name}={value!r}" for (name, value) in self.kwargs.items()]
        return f"{clsname}({', '.join(arg_strings)})"

    def matches(self, target: Any):
        return all([func(target) for func in self.matchers])

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def then(self, **rules):
        return Transformation(query=self, rules=rules)


class And(BaseQuery):
    def __init__(self, *queries):
        self.queries = queries

    def matches(self, target: Any):
        return all([q.matches(target) for q in self.queries])


class Or(BaseQuery):
    def __init__(self, *queries):
        self.queries = queries

    def matches(self, target: Any):
        return any([q.matches(target) for q in self.queries])
