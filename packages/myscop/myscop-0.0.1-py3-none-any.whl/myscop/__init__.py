from typing import Iterable

from more_itertools import always_iterable, repeat_last
from scop import Linear, Model


class MyModel(Model):
    def addvars(self, num: int, dom: Iterable):
        return [self.addVariable(f"v_{i:03}", dom) for i in range(num)]

    def addcons(self, weight, constr):
        self.addConstraint(constr.constr(weight))


class MyLinear:
    def __init__(self, coe, var, val):
        self.coe = coe
        self.var = var
        self.val = val if isinstance(0, Iterable) else repeat_last(always_iterable(val))
        self.rhs = 0
        self.direction = "<="

    def __eq__(self, rhs):
        self.rhs = rhs
        self.direction = "="
        return self

    def __ge__(self, rhs):
        self.rhs = rhs
        self.direction = ">="
        return self

    def __le__(self, rhs):
        self.rhs = rhs
        self.direction = "<="
        return self

    def constr(self, weight):
        cn = Linear(weight=weight, rhs=self.rhs, direction=self.direction)
        for c, vr, vl in zip(self.coe, self.var, self.val):
            cn.addTerms(c, vr, vl)
        return cn
