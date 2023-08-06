import abc
import math
from copy import copy
from typing import Iterable, List, Union

import pandas as pd
from more_itertools import always_iterable, repeat_last
from scop import Alldiff, Linear, Model, Quadratic

inf = math.inf


def to_list(it, ref):
    if not isinstance(it, str) and isinstance(it, Iterable):
        return it if isinstance(it, list) else list(it)
    return [i for i, _ in zip(repeat_last(always_iterable(it)), ref)]


class MyExpr(metaclass=abc.ABCMeta):
    type_: type = type
    args: List[str] = []

    @abc.abstractmethod
    def __add__(self, other):
        pass

    @abc.abstractmethod
    def __sub__(self, other):
        pass

    def to_constr(self, rhs, direction):
        assert isinstance(rhs, int) or isinstance(rhs, float)
        return MyConstraint(self, rhs, direction)

    def __eq__(self, rhs):
        return self.to_constr(rhs, "=")

    def __ge__(self, rhs):
        return self.to_constr(rhs, ">=")

    def __le__(self, rhs):
        return self.to_constr(rhs, "<=")

    def append(self, coe, other):
        expr = copy(self)  # 再代入するのでdeepcopyでなくてよい
        for arg in self.args:
            v1, v2 = getattr(expr, arg), getattr(other, arg)
            if arg == "coe" and coe != 1:
                v2 = [coe * i for i in v2]
            setattr(expr, arg, v1 + v2)
        return expr


class MyConstraint:
    rhs: float = 0
    direction: str = "<="

    def __init__(self, expr, rhs, direction):
        self.type_ = expr.type_
        self.args = expr.args
        for arg in expr.args:
            setattr(self, arg, getattr(expr, arg))
        self.rhs = rhs
        self.direction = direction

    def scop_constr(self, name, weight):
        dc = dict(name=name, weight=weight)
        if self.type_ != Alldiff:
            dc.update(rhs=self.rhs, direction=self.direction)
        cn = self.type_(**dc)
        if self.type_ != Alldiff:
            for x in zip(*(getattr(self, arg) for arg in self.args)):
                cn.addTerms(*x)
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
        assert isinstance(constr, MyConstraint)
        self.addConstraint(constr.scop_constr(name, weight))

    def addvals(
        self, dfs: Union[pd.DataFrame, list], var: str = "Var", val: str = "Val"
    ):
        if isinstance(dfs, pd.DataFrame):
            dfs = [dfs]
        for df in dfs:
            df[val] = [v.value for v in df[var]]


class MyLinear(MyExpr):
    type_ = Linear
    args = ["coe", "var", "val"]

    def __init__(self, coe, var, val):
        self.coe = to_list(coe, var)  # first args of addTerms, not weight
        self.var = var
        self.val = to_list(val, var)

    def __add__(self, other):
        assert isinstance(other, MyLinear)
        return self.append(1, other)

    def __sub__(self, other):
        assert isinstance(other, MyLinear)
        return self.append(-1, other)


class MyQuadratic(MyExpr):
    type_ = Quadratic
    args = ["coe", "var1", "val1", "var2", "val2"]

    def __init__(self, coe, var1, val1, var2, val2):
        assert len(var1) == len(var2)
        self.coe = to_list(coe, var1)  # first args of addTerms, not weight
        self.var1 = var1
        self.val1 = to_list(val1, var1)
        self.var2 = var2
        self.val2 = to_list(val2, var1)

    def __add__(self, other):
        assert isinstance(other, MyQuadratic)
        return self.append(1, other)

    def __sub__(self, other):
        assert isinstance(other, MyQuadratic)
        return self.append(-1, other)


class MyAlldiff(MyConstraint):
    type_ = Alldiff
    args = ["var"]

    def __init__(self, var):
        self.var = var
