"""Statistics computed incrementally over sequences"""
from __future__ import annotations

import math
from typing import Generic, Iterable, Tuple, TypeVar

__all__ = [
    "ExponentialMovingAverage",
    "ScalingExponentialMovingAverage",
    "SequenceAverage",
    "SequenceMean",
    "SequenceStatistic",
]

_T = TypeVar("_T")
_U = TypeVar("_U")


class SequenceStatistic(Generic[_T, _U]):
    """A statistic computed incrementally over a sequence."""

    @property
    def value(self) -> _U:
        """The current value of the statistic"""

    def append(self, value: _T) -> None:
        """Append a new value to the sequence."""
        raise NotImplementedError

    def extend(self, values: Iterable[_T]):
        for value in values:
            self.append(value)


class SequenceAverage(SequenceStatistic[float, float]):
    """A weighted average

    O(1) memory
    """

    def __init__(self):
        super().__init__()
        self._len = 0
        # Scale is calculated the same way as _total but as if all inputs were 1
        # This serves as a normalizing factor on the computed average.
        self._total: float = 0
        self._scale: float = 0

    @property
    def value(self) -> float:
        return self._total / self._scale

    def append(self, value: float) -> None:
        self._len += 1
        total_weight, value_weight = self._weights()
        self._total *= total_weight
        self._total += value_weight * value
        self._scale *= total_weight
        self._scale += value_weight

    def _weights(self) -> Tuple[float, float]:
        raise NotImplementedError


class SequenceMean(SequenceAverage):
    """The mean of all elements in a sequence."""

    def _weights(self):
        value_weight = 1 / self._len
        return 1 - value_weight, value_weight


class ExponentialMovingAverage(SequenceAverage):
    """An exponential moving average"""

    def __init__(self, discount_factor: float):
        """Initialize an ExponentialMovingAverage

        Args:
            discount_factor: The scaling factor applied to previous values on each step.
                Should be in [0, 1].
        """
        super().__init__()
        self.discount_factor = discount_factor

    def _weights(self):
        return self.discount_factor, 1 - self.discount_factor


class ScalingExponentialMovingAverage(SequenceAverage):
    """An exponential-like moving average summarizing a constant fraction of the data."""

    def __init__(self, data_fraction: float, weight_threshold: float = 0.9):
        """Initialize a ScalingExponentialMovingAverage

        Args:
            data_fraction: Approximately what fraction of the data to include.
                A suffix of the sequence is considered to be included in the average
                if the sum of normalized coefficients on those elements is at least
                `weight_threshold`. A value in [0, 1]
            weight_threshold: The sum of normalized coefficients on sequence data
                must be at least this much for a suffix of the sequence to be considered
                represented in the average.
        """
        super().__init__()
        self._log_beta = math.log(1 - weight_threshold) / data_fraction

    def _weights(self):
        total_weight = math.exp(self._log_beta / self._len)
        return total_weight, 1 - total_weight
