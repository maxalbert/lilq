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


class Q(BaseQuery):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __repr__(self):
        clsname = self.__class__.__name__
        arg_strings = [f"{name}={value!r}" for (name, value) in self.kwargs.items()]
        return f"{clsname}({', '.join(arg_strings)})"

    def matches(self, target: Any):
        return all([getattr(target, attr_name) == value for (attr_name, value) in self.kwargs.items()])

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
