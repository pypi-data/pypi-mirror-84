"""Test Sequence Statistics"""
from __future__ import annotations

import functools
import math

import pytest

from cmot.sequence_statistics import (
    ExponentialMovingAverage,
    ScalingExponentialMovingAverage,
    SequenceAverage,
    SequenceMean,
)


@pytest.fixture(
    ids=[
        "SequenceMean",
        "ExponentialMovingAverage(0.9)",
        "ScalingExponentialMovingAverage(0.1)",
    ],
    params=[
        SequenceMean,
        functools.partial(ExponentialMovingAverage, 0.9),
        functools.partial(ScalingExponentialMovingAverage, 0.1),
    ],
)
def sequence_average(request) -> SequenceAverage:
    return request.param()


@pytest.fixture
def sema10() -> ScalingExponentialMovingAverage:
    return ScalingExponentialMovingAverage(0.1)


def test_sequence_average_interpolates(sequence_average: SequenceAverage):
    sequence_average.append(2)
    assert sequence_average.value == 2
    sequence_average.append(4)
    assert 2 <= sequence_average.value <= 4
    sequence_average.append(-10)
    assert -10 <= sequence_average.value <= 4


def test_sequence_average_ones(sequence_average: SequenceAverage):
    sequence_average.extend([1] * 10000)
    assert math.isclose(sequence_average.value, 1)


def test_sequence_mean():
    a = SequenceMean()
    a.extend(range(10))
    assert math.isclose(a.value, 4.5)


def test_exponential_moving_average():
    a = ExponentialMovingAverage(0.8)
    a.extend(range(1, 4))
    assert math.isclose(a.value, (0.8 ** 2 * 1 + 0.8 * 2 + 3) / (0.8 ** 2 + 0.8 + 1))


@pytest.mark.parametrize("n", [10, 100, 1000])
def test_scaling_exponential_moving_average(
    sema10: ScalingExponentialMovingAverage, n: int
):
    # The sema10 value should always represent that last 10% of the data, no matter the
    # amount of data.
    sema10.extend(range(1, n + 1))
    assert 0.9 * n < sema10.value < n
