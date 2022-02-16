"""An experiment with n-ary logic"""

from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from math import ceil, log


@dataclass(order=True, slots=True, frozen=True)
class NAryDigit:
    value: int
    n: int = 2

    def __post_init__(self):
        if not (0 <= self.value < self.n):
            raise ValueError(f"Value must be in [0, {self.n})")

    def validate(self, other):
        if self.n != other.n:
            raise ValueError("Incompatible digits: "
                             f"{repr(self)} and {repr(other)}")

    def __invert__(self):
        return self.__class__(self.n - self.value - 1, n=self.n)

    def __or__(self, other):
        self.validate(other)

        return self.__class__(max(self.value, other.value), n=self.n)

    def __and__(self, other):
        self.validate(other)

        return self.__class__(min(self.value, other.value), n=self.n)

    def __xor__(self, other):
        return (self | other) & ~(self & other)

    def __str__(self):
        return str(self.value)

    def __format__(self, fmt: str) -> str:
        return f"{self.value:{fmt}}"


class TruthTable:
    def __init__(self, op, n=2) -> None:
        self.op = op
        self.n = n

        self.truth_table = tuple(
            tuple(op(NAryDigit(i, n=n), NAryDigit(j, n=n))
                  for j in range(n))
            for i in range(n))

    def __str__(self) -> str:
        w = ceil(log(self.n, 10))

        # Capture prints to string
        with redirect_stdout(StringIO()) as s:
            print(" "*(w + 1) + "| ", end="")
            print(" ".join(f"{i:{w}}" for i in range(self.n)))
            print("-"*((1 + self.n)*(w + 1) + 1))
            for i, row in enumerate(self.truth_table):
                print(f"{i:>{w}} | ", end="")
                for j, cell in enumerate(row):
                    print(f"{cell:>{w}}", end=" ")
                print()
        s.seek(0)

        return s.read()
