import math
from copy import copy
from typing import Iterable, List, Union

import pandas as pd
from more_itertools import always_iterable, repeat_last
from scop import Alldiff, Linear, Model, Quadratic

inf = math.inf


def to_iter(it, var):
    if not isinstance(it, str) and isinstance(it, Iterable):
        return it
    return [i for i, _ in zip(repeat_last(always_iterable(it)), var)]


class MyConstraint:
    type_: type = type
    args: List[str] = []
    rhs: float = 0
    direction: str = "<="

    def constr(self, rhs, direction):
        cn = copy(self)
        if isinstance(rhs, MyLinear):
            assert isinstance(self, MyLinear)
            cn.coe.extend([-i for i in rhs.coe])
            cn.var.extend(rhs.var)
            cn.val.extend(rhs.val)
            rhs = 0
        assert isinstance(rhs, int) or isinstance(rhs, float)
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
    def addvars(
        self,
        num: Union[int, pd.DataFrame],
        domain: Iterable,
        pre: str = "v_",
        start: int = 0,
        var: str = "Var",
    ):
        n, df = num, None
        if isinstance(num, pd.DataFrame):
            n, df = len(num), num
        v = [self.addVariable(f"{pre}{i + start:03}", domain) for i in range(n)]
        if df is not None:
            df[var] = v
        return v

    def addcons(self, constr: MyConstraint, name: str = "", weight: float = 1):
        self.addConstraint(constr.eval(name, weight))

    def addvals(
        self, dfs: Union[pd.DataFrame, list], var: str = "Var", val: str = "Val"
    ):
        if isinstance(dfs, pd.DataFrame):
            dfs = [dfs]
        for df in dfs:
            df[val] = [v.value for v in df[var]]


class MyLinear(MyConstraint):
    type_ = Linear
    args = ["coe", "var", "val"]

    def __init__(self, coe, var, val):
        self.coe = to_iter(coe, var)  # first args of addTerms, not weight
        self.var = var
        self.val = to_iter(val, var)


class MyQuadratic(MyConstraint):
    type_ = Quadratic
    args = ["coe", "var1", "val1", "var2", "val2"]

    def __init__(self, coe, var1, val1, var2, val2):
        assert len(var1) == len(var2)
        self.coe = to_iter(coe, var1)  # first args of addTerms, not weight
        self.var1 = var1
        self.val1 = to_iter(val1, var1)
        self.var2 = var2
        self.val2 = to_iter(val2, var1)


class MyAlldiff(MyConstraint):
    type_ = Alldiff
    args = ["var"]

    def __init__(self, var):
        self.var = var
