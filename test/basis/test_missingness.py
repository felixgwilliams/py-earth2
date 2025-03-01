from __future__ import annotations

import pickle

import numpy

from pyearth._basis import (
    ConstantBasisFunction,
    HingeBasisFunction,
    MissingnessBasisFunction,
)
from pyearth._types import BOOL

from . import assert_equal, assert_true
from .base import BaseContainer


class Container(BaseContainer):
    def __init__(self):
        super(Container, self).__init__()
        self.parent = ConstantBasisFunction()
        self.bf = MissingnessBasisFunction(self.parent, 1, True)
        self.child = HingeBasisFunction(self.bf, 1.0, 10, 1, False)


#
# def test_getters():
#     cnt = Container()
#     assert not cnt.bf.get_reverse()
#     assert cnt.bf.get_knot() == 1.0
#     assert cnt.bf.get_variable() == 1
#     assert cnt.bf.get_knot_idx() == 10
#     assert cnt.bf.get_parent() == cnt.parent


def test_apply():
    cnt = Container()
    m, _ = cnt.X.shape
    missing = numpy.zeros_like(cnt.X, dtype=BOOL)
    missing[1, 1] = True
    B = numpy.ones(shape=(m, 10))
    X = cnt.X.copy()
    X[1, 1] = None
    cnt.bf.apply(cnt.X, missing, B[:, 0])
    numpy.testing.assert_almost_equal(B[:, 0], 1 - missing[:, 1])
    cnt.child.apply(cnt.X, missing, B[:, 0])
    expected = (cnt.X[:, 1] - 1.0) * (cnt.X[:, 1] > 1.0)
    expected[1] = 0.0
    numpy.testing.assert_almost_equal(B[:, 0], expected)


# def test_apply_deriv():
#     cnt = Container()
#     m, _ = cnt.X.shape
#     missing = numpy.zeros_like(cnt.X, dtype=BOOL)
#     b = numpy.empty(shape=m)
#     j = numpy.empty(shape=m)
#     cnt.bf.apply_deriv(cnt.X, missing, b, j, 1)
#     numpy.testing.assert_almost_equal(
#         (cnt.X[:, 1] - 1.0) * (cnt.X[:, 1] > 1.0),
#         b
#     )
#     numpy.testing.assert_almost_equal(1.0 * (cnt.X[:, 1] > 1.0), j)


def test_degree():
    cnt = Container()
    assert_equal(cnt.bf.degree(), 1)


def test_pickle_compatibility():
    cnt = Container()
    bf_copy = pickle.loads(pickle.dumps(cnt.bf))
    assert_true(cnt.bf == bf_copy)


#
# def test_smoothed_version():
#     cnt = Container()
#     knot_dict = {cnt.bf: (.5, 1.5)}
#     translation = {cnt.parent: cnt.parent._smoothed_version(None, {}, {})}
#     smoothed = cnt.bf._smoothed_version(cnt.parent, knot_dict,
#                                         translation)
#
#     assert_true(type(smoothed) is SmoothedHingeBasisFunction)
#     assert_true(translation[cnt.parent] is smoothed.get_parent())
#     assert_equal(smoothed.get_knot_minus(), 0.5)
#     assert_equal(smoothed.get_knot_plus(), 1.5)
#     assert_equal(smoothed.get_knot(), cnt.bf.get_knot())
#     assert_equal(smoothed.get_variable(), cnt.bf.get_variable())
