import numpy

import numpy_ipps._detail.dispatch


class Unary(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps._detail.dispatch.keep_all,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:
            attrs["__slots__"] = attrs["__slots__"] + ("_ipps_callback_64",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls._ipps_policies = policies

        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:

            def cls_ipps_backend_64(self, src_cdata, dst_cdata, dst_size):
                return self._ipps_callback_64(
                    src_cdata, dst_cdata, 2 * int(dst_size)
                )

            cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_numpy_backend(self, src, dst):
            numpy_backend(src.ndarray, dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        def cls__call__(self, src, dst):
            assert (
                src.ndarray.size == dst.ndarray.size
            ), "src and dst size not compatible."

            numpy_ipps.status = self._ipps_backend(
                src.cdata, dst.cdata, dst.size
            )

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype=numpy.uint32):
        self = super().__call__()

        if (
            cls._ipps_policies.bytes8[0]
            in numpy_ipps._detail.dispatch.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                ("void*", "void*", "int"),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                ("void*", "void*", "int"),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class Unary_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps._detail.dispatch.keep_all,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:
            attrs["__slots__"] = attrs["__slots__"] + ("_ipps_callback_64",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls._ipps_policies = policies

        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:

            def cls_ipps_backend_64(self, src_dst_cdata, src_dst_size):
                return self._ipps_callback_64(
                    src_dst_cdata, 2 * int(src_dst_size)
                )

            cls._ipps_backend_64 = cls_ipps_backend_64

        def cls_numpy_backend(self, src_dst):
            numpy_backend(src_dst.ndarray, src_dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        def cls__call__(self, src_dst):
            numpy_ipps.status = self._ipps_backend(src_dst.cdata, src_dst.size)

        cls.__call__ = cls__call__

        return cls

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)

    def __call__(cls, dtype=numpy.uint32):
        self = super().__call__()

        if (
            cls._ipps_policies.bytes8[0]
            in numpy_ipps._detail.dispatch.down_tags
            and numpy.dtype(dtype).itemsize == 8
        ):
            self._ipps_callback_64 = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                ("void*", "int"),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                ("void*", "int"),
                dtype,
                policies=cls._ipps_policies,
            )

        return self
