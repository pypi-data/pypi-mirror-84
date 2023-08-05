"""Logical Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries


_logical_policies = _dispatch.Policies(
    bytes1=_dispatch.TagPolicy.UNSIGNED,
    bytes2=_dispatch.TagPolicy.UNSIGNED,
    bytes4=_dispatch.TagPolicy.UNSIGNED,
    bytes8=_dispatch.TagPolicy.DOWN_UNSIGNED,
)


class And(
    metaclass=_binaries.Binary,
    ipps_backend="And",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
):
    """And Function."""

    pass


class And_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="And_I",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
):
    """And_I Function."""

    pass


class AndC(
    metaclass=_binaries.BinaryC,
    ipps_backend="AndC",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
):
    """AndC Function."""

    pass


class AndC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="AndC_I",
    numpy_backend=_numpy.bitwise_and,
    policies=_logical_policies,
):
    """AndC_I Function."""

    pass


class Or(
    metaclass=_binaries.Binary,
    ipps_backend="Or",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
):
    """Or Function."""

    pass


class Or_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Or_I",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
):
    """Or_I Function."""

    pass


class OrC(
    metaclass=_binaries.BinaryC,
    ipps_backend="OrC",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
):
    """OrC Function."""

    pass


class OrC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="OrC_I",
    numpy_backend=_numpy.bitwise_or,
    policies=_logical_policies,
):
    """OrC_I Function."""

    pass


class Xor(
    metaclass=_binaries.Binary,
    ipps_backend="Xor",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
):
    """Xor Function."""

    pass


class Xor_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Xor_I",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
):
    """Xor_I Function."""

    pass


class XorC(
    metaclass=_binaries.BinaryC,
    ipps_backend="XorC",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
):
    """XorC Function."""

    pass


class XorC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="XorC_I",
    numpy_backend=_numpy.bitwise_xor,
    policies=_logical_policies,
):
    """XorC_I Function."""

    pass


class LShiftC(
    metaclass=_binaries.BinaryC,
    ipps_backend="LShiftC",
    numpy_backend=_numpy.left_shift,
):
    """LShiftC Function."""

    pass


class LShiftC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="LShiftC_I",
    numpy_backend=_numpy.left_shift,
):
    """LShiftC_I Function."""

    pass


class RShiftC(
    metaclass=_binaries.BinaryC,
    ipps_backend="RShiftC",
    numpy_backend=_numpy.right_shift,
):
    """RShiftC Function."""

    pass


class RShiftC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="RShiftC_I",
    numpy_backend=_numpy.right_shift,
):
    """RShiftC_I Function."""

    pass


class Not(
    metaclass=_unaries.Unary,
    ipps_backend="Not",
    numpy_backend=_numpy.invert,
    policies=_logical_policies,
):
    """Not Function."""

    pass


class Not_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Not_I",
    numpy_backend=_numpy.invert,
    policies=_logical_policies,
):
    """Not_I Function."""

    pass
