import importlib
import logging
import os

import numpy
import psutil
import pytest

import numpy_ipps
import numpy_ipps.utils


max_cache_size = psutil.virtual_memory().total
orders = range(4, int(numpy.floor(numpy.log2(max_cache_size))) - 6, 2)
dtypes_abs = (numpy.int16, numpy.int32)
dtypes_add = (
    numpy.int16,
    numpy.uint16,
    numpy.int32,
    numpy.uint32,
)
dtypes_mul = (numpy.int16,)
dtypes_sub = (
    numpy.int16,
    numpy.uint16,
)


@pytest.fixture(scope="module")
def logger_fixture(pytestconfig):
    logger = logging.getLogger("numpy_ipps")
    logger.setLevel(logging.DEBUG)

    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "log_ref",
        "test_integer.log",
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(ch)
    importlib.reload(numpy_ipps)

    yield logger

    logger.removeHandler(ch)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_ipps_addcI(logger_fixture, benchmark, order, dtype):
    addc_I = numpy_ipps.AddIntegerC_I(dtype=dtype)
    value = 0
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(addc_I, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_numpy_addcI(logger_fixture, benchmark, order, dtype):
    addc_I = numpy_ipps.AddIntegerC_I(dtype=dtype)
    value = 0
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(addc_I._numpy_backend, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_mul)
def test_ipps_mulcI(logger_fixture, benchmark, order, dtype):
    mulc_I = numpy_ipps.MulIntegerC_I(dtype=dtype)
    value = 0
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(mulc_I, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_mul)
def test_numpy_mulcI(logger_fixture, benchmark, order, dtype):
    mulc_I = numpy_ipps.MulIntegerC_I(dtype=dtype)
    value = 0
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(mulc_I._numpy_backend, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_ipps_subcI(logger_fixture, benchmark, order, dtype):
    subc_I = numpy_ipps.SubIntegerC_I(dtype=dtype)
    value = 0
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(subc_I, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_numpy_subcI(logger_fixture, benchmark, order, dtype):
    subc_I = numpy_ipps.SubIntegerC_I(dtype=dtype)
    value = 0
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(subc_I._numpy_backend, value, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_add)
def test_ipps_add(logger_fixture, benchmark, order, dtype):
    addb = numpy_ipps.AddInteger(dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(addb, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 2)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_add)
def test_ipps_addI(logger_fixture, benchmark, order, dtype):
    addb_I = numpy_ipps.AddInteger_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(addb_I, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_add)
def test_numpy_add(logger_fixture, benchmark, order, dtype):
    addb = numpy_ipps.AddInteger(dtype=dtype)
    src1 = numpy.ones(1 << order, dtype=dtype)
    src2 = numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(addb._numpy_backend, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 2)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_add)
def test_numpy_addI(logger_fixture, benchmark, order, dtype):
    addb_I = numpy_ipps.AddInteger_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(addb_I._numpy_backend, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_mul)
def test_ipps_mul(logger_fixture, benchmark, order, dtype):
    mulb = numpy_ipps.MulInteger(dtype=dtype)
    src1 = 2 * numpy.ones(1 << order, dtype=dtype)
    src2 = 2 * numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(mulb, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 4)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_mul)
def test_ipps_mulI(logger_fixture, benchmark, order, dtype):
    mulb_I = numpy_ipps.MulInteger_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(mulb_I, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_mul)
def test_numpy_mul(logger_fixture, benchmark, order, dtype):
    mulb = numpy_ipps.MulInteger(dtype=dtype)
    src1 = 2 * numpy.ones(1 << order, dtype=dtype)
    src2 = 2 * numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(mulb._numpy_backend, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 4)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_mul)
def test_numpy_mulI(logger_fixture, benchmark, order, dtype):
    mulb_I = numpy_ipps.MulInteger_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(mulb_I._numpy_backend, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 0)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_ipps_sub(logger_fixture, benchmark, order, dtype):
    subb = numpy_ipps.SubInteger(dtype=dtype)
    src1 = 2 * numpy.ones(1 << order, dtype=dtype)
    src2 = 4 * numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(subb, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 2)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_ipps_subI(logger_fixture, benchmark, order, dtype):
    subb_I = numpy_ipps.SubInteger_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(subb_I, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_numpy_sub(logger_fixture, benchmark, order, dtype):
    subb = numpy_ipps.SubInteger(dtype=dtype)
    src1 = 2 * numpy.ones(1 << order, dtype=dtype)
    src2 = 4 * numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src1, src2, dst):
        benchmark(subb._numpy_backend, src1, src2, dst)

    numpy.testing.assert_almost_equal(dst, 2)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_sub)
def test_numpy_subI(logger_fixture, benchmark, order, dtype):
    subb_I = numpy_ipps.SubInteger_I(dtype=dtype)
    src = numpy.zeros(1 << order, dtype=dtype)
    src_dst = numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, src_dst):
        benchmark(subb_I._numpy_backend, src, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_abs)
def test_ipps_abs(logger_fixture, benchmark, order, dtype):
    absu = numpy_ipps.AbsInteger(dtype=dtype)
    src = -numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(absu, src, dst)

    numpy.testing.assert_almost_equal(dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_abs)
def test_ipps_absI(logger_fixture, benchmark, order, dtype):
    absu_I = numpy_ipps.AbsInteger_I(dtype=dtype)
    src_dst = -numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(absu_I, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_abs)
def test_numpy_abs(logger_fixture, benchmark, order, dtype):
    absu = numpy_ipps.AbsInteger(dtype=dtype)
    src = -numpy.ones(1 << order, dtype=dtype)
    dst = numpy.empty(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src, dst):
        benchmark(absu._numpy_backend, src, dst)

    numpy.testing.assert_almost_equal(dst, 1)


@pytest.mark.parametrize("order", orders)
@pytest.mark.parametrize("dtype", dtypes_abs)
def test_numpy_absI(logger_fixture, benchmark, order, dtype):
    absu_I = numpy_ipps.AbsInteger_I(dtype=dtype)
    src_dst = -numpy.ones(1 << order, dtype=dtype)

    with numpy_ipps.utils.context(src_dst):
        benchmark(absu_I._numpy_backend, src_dst)

    numpy.testing.assert_almost_equal(src_dst, 1)
