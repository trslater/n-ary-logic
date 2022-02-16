"""An experiment with n-ary logic"""

from dataclasses import dataclass


@dataclass(order=True, slots=True, frozen=True)
class NAryDigit:
    value: int
    n: int = 2

    def __post_init__(self):
        if not (0 <= self.value < self.n):
            raise ValueError(f"Value must be in [0, {self.n})")

    def __invert__(self):
        return self.__class__(self.n - self.value - 1, n=self.n)

    def __or__(self, other):
        return self.__class__(max(self.value, other.value), n=self.n)

    def __and__(self, other):
        return self.__class__(min(self.value, other.value), n=self.n)

    def __xor__(self, other):
        return (self | other) & ~(self & other)

    def __str__(self):
        return str(self.value)
