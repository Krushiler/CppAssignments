from __future__ import annotations
from typing import Protocol
from array import array


class Collection(Protocol):
    @staticmethod
    def zeros(size: array) -> Collection:
        pass

    @staticmethod
    def ones(size: array) -> Collection:
        pass

    @staticmethod
    def randoms(size: array) -> Collection:
        pass

    def size(self) -> float:
        pass

    def mean(self, size: array) -> float:
        pass

    def transpose(self) -> None:
        pass

    def min(self) -> float:
        pass

    def max(self) -> float:
        pass

    def __rmul__(self, other: Collection) -> Collection:
        pass

    def __mul__(self, other) -> Collection:
        pass

