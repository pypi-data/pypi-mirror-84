from copy import copy
from typing import Iterable, List

from more_itertools import always_iterable, repeat_last
from scop import Alldiff, Linear, Model, Quadratic


def to_iter(i):
    return i if isinstance(i, Iterable) else repeat_last(always_iterable(i))


class MyConstraint:
    type_: type = type
    args: List[str] = []
    rhs: float = 0
    direction: str = "<="

    def constr(self, rhs, direction):
        cn = copy(self)
        cn.rhs, cn.direction = rhs, direction
        return cn

    def __eq__(self, rhs):
        return self.constr(rhs, "=")

    def __ge__(self, rhs):
        return self.constr(rhs, ">=")

    def __le__(self, rhs):
        return self.constr(rhs, "<=")

    def eval(self, name, weight):
        dc = dict(name=name, weight=weight)
        if self.type_ != Alldiff:
            dc.update(rhs=self.rhs, direction=self.direction)
        cn = self.type_(**dc)
        if self.type_ != Alldiff:
            for a in zip(*(getattr(self, a) for a in self.args)):
                cn.addTerms(*a)
        else:
            for v in getattr(self, *self.args):
                cn.addVariable(v)
        return cn


class MyModel(Model):
    def addvars(self, num: int, dom: Iterable):
        return [self.addVariable(f"v_{i:03}", dom) for i in range(num)]

    def addcons(self, constr: MyConstraint, name: str = "", weight: float = 1):
        self.addConstraint(constr.eval(name, weight))


class MyLinear(MyConstraint):
    type_ = Linear
    args = ["coe", "var", "val"]

    def __init__(self, coe, var, val):
        self.coe = to_iter(coe)  # first args of addTerms, not weight
        self.var = var
        self.val = to_iter(val)


class MyQuadratic(MyConstraint):
    type_ = Quadratic
    args = ["coe", "var1", "val1", "var2", "val2"]

    def __init__(self, coe, var1, val1, var2, val2):
        self.coe = to_iter(coe)  # first args of addTerms, not weight
        self.var1 = var1
        self.val1 = to_iter(val1)
        self.var2 = var2
        self.val2 = to_iter(val2)


class MyAlldiff(MyConstraint):
    type_ = Alldiff
    args = ["var"]

    def __init__(self, var):
        self.var = var
