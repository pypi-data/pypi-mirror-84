"""Arithmetic Integer Functions."""
import numpy as _numpy

import numpy_ipps._detail.dispatch as _dispatch
import numpy_ipps._detail.metaclass.binaries as _binaries
import numpy_ipps._detail.metaclass.unaries as _unaries


# Not implemented
"""
IppStatus ippsAdd_8u16u
    (const Ipp8u* pSrc1, const Ipp8u* pSrc2, Ipp16u* pDst, int len);
IppStatus ippsAdd_16s32f
    (const Ipp16s* pSrc1, const Ipp16s* pSrc2, Ipp32f* pDst, int len);

IppStatus ippsMul_8u16u
    (const Ipp8u* pSrc1, const Ipp8u* pSrc2, Ipp16u* pDst, int len);
"""


class AddInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Add",
    numpy_backend=_numpy.add,
    policies=_dispatch.Policies(
        bytes1=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes2=_dispatch.TagPolicy.KEEP,
        bytes4=_dispatch.TagPolicy.UNSIGNED,
        bytes8=_dispatch.TagPolicy.NOT_IMPLEMENTED,
    ),
):
    """Add Function."""

    pass


class AddInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Add_I",
    numpy_backend=_numpy.add,
    policies=_dispatch.Policies(
        bytes1=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes2=_dispatch.TagPolicy.SIGNED,
        bytes4=_dispatch.TagPolicy.UNSIGNED,
        bytes8=_dispatch.TagPolicy.NOT_IMPLEMENTED,
    ),
):
    """Add_I Function."""

    pass


class AddIntegerC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="AddC_I",
    numpy_backend=_numpy.add,
    policies=_dispatch.Policies(
        bytes1=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes2=_dispatch.TagPolicy.SIGNED,
        bytes4=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes8=_dispatch.TagPolicy.NOT_IMPLEMENTED,
    ),
):
    """AddC_I Function."""

    pass


class MulInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Mul",
    numpy_backend=_numpy.multiply,
):
    """Mul Function."""

    pass


class MulInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Mul_I",
    numpy_backend=_numpy.multiply,
):
    """Mul_I Function."""

    pass


class MulIntegerC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="MulC_I",
    numpy_backend=_numpy.multiply,
):
    """MulC_I Function."""

    pass


class SubInteger(
    metaclass=_binaries.Binary,
    ipps_backend="Sub",
    numpy_backend=_numpy.subtract,
    policies=_dispatch.Policies(
        bytes1=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes2=_dispatch.TagPolicy.SIGNED,
        bytes4=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes8=_dispatch.TagPolicy.NOT_IMPLEMENTED,
    ),
    numpy_swap=True,
):
    """Sub Function."""

    pass


class SubInteger_I(
    metaclass=_binaries.Binary_I,
    ipps_backend="Sub_I",
    numpy_backend=_numpy.subtract,
    policies=_dispatch.Policies(
        bytes1=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes2=_dispatch.TagPolicy.SIGNED,
        bytes4=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes8=_dispatch.TagPolicy.NOT_IMPLEMENTED,
    ),
    numpy_swap=True,
):
    """Sub_I Function."""

    pass


class SubIntegerC_I(
    metaclass=_binaries.BinaryC_I,
    ipps_backend="SubC_I",
    numpy_backend=_numpy.subtract,
    policies=_dispatch.Policies(
        bytes1=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes2=_dispatch.TagPolicy.SIGNED,
        bytes4=_dispatch.TagPolicy.NOT_IMPLEMENTED,
        bytes8=_dispatch.TagPolicy.NOT_IMPLEMENTED,
    ),
):
    """SubC_I Function."""

    pass


class AbsInteger(
    metaclass=_unaries.Unary,
    ipps_backend="Abs",
    numpy_backend=_numpy.fabs,
):
    """Abs Function."""

    pass


class AbsInteger_I(
    metaclass=_unaries.Unary_I,
    ipps_backend="Abs_I",
    numpy_backend=_numpy.fabs,
):
    """Abs_I Function."""

    pass
