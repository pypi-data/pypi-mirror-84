import numpy

import numpy_ipps._detail.dispatch


class Binary(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps._detail.dispatch.keep_all,
        numpy_swap=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:
            attrs["__slots__"] = attrs["__slots__"] + ("_ipps_callback_64",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls._ipps_policies = policies

        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:

            def cls_ipps_backend_64(
                self, src1_cdata, src2_cdata, dst_cdata, dst_size
            ):
                return self._ipps_callback_64(
                    src1_cdata, src2_cdata, dst_cdata, 2 * int(dst_size)
                )

            cls._ipps_backend_64 = cls_ipps_backend_64

        if numpy_swap:

            def cls_numpy_backend(self, src1, src2, dst):
                numpy_backend(
                    src2.ndarray, src1.ndarray, dst.ndarray, casting="unsafe"
                )

        else:

            def cls_numpy_backend(self, src1, src2, dst):
                numpy_backend(
                    src1.ndarray, src2.ndarray, dst.ndarray, casting="unsafe"
                )

        cls._numpy_backend = cls_numpy_backend

        def cls__call__(self, src1, src2, dst):
            assert (
                src1.ndarray.size == dst.ndarray.size
            ), "src and dst size not compatible."
            assert (
                src2.ndarray.size == dst.ndarray.size
            ), "src and dst size not compatible."

            numpy_ipps.status = self._ipps_backend(
                src1.cdata, src2.cdata, dst.cdata, dst.size
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
                ("void*", "void*", "void*", "int"),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                ("void*", "void*", "void*", "int"),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class Binary_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps._detail.dispatch.keep_all,
        numpy_swap=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:
            attrs["__slots__"] = attrs["__slots__"] + ("_ipps_callback_64",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls._ipps_policies = policies

        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:

            def cls_ipps_backend_64(
                self, src_cdata, src_dst_cdata, src_dst_size
            ):
                return self._ipps_callback_64(
                    src_cdata, src_dst_cdata, 2 * int(src_dst_size)
                )

            cls._ipps_backend_64 = cls_ipps_backend_64

        if numpy_swap:

            def cls_numpy_backend(self, src, src_dst):
                assert (
                    src.ndarray.size == src_dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_backend(
                    src_dst.ndarray,
                    src.ndarray,
                    src_dst.ndarray,
                    casting="unsafe",
                )

        else:

            def cls_numpy_backend(self, src, src_dst):
                assert (
                    src.ndarray.size == src_dst.ndarray.size
                ), "src and dst size not compatible."

                numpy_backend(
                    src.ndarray,
                    src_dst.ndarray,
                    src_dst.ndarray,
                    casting="unsafe",
                )

        cls._numpy_backend = cls_numpy_backend

        def cls__call__(self, src, src_dst):
            assert (
                src.ndarray.size == src_dst.ndarray.size
            ), "src and dst size not compatible."

            numpy_ipps.status = self._ipps_backend(
                src.cdata, src_dst.cdata, src_dst.size
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


class BinaryC(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps._detail.dispatch.keep_all,
        numpy_swap=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:
            attrs["__slots__"] = attrs["__slots__"] + ("_ipps_callback_64",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls._ipps_policies = policies

        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:

            def cls_ipps_backend_64(self, src_cdata, val, dst_cdata, dst_size):
                return self._ipps_callback_64(
                    src_cdata, val, dst_cdata, 2 * int(dst_size)
                )

            cls._ipps_backend_64 = cls_ipps_backend_64

        if numpy_swap:

            def cls_numpy_backend(self, src, val, dst):
                numpy_backend(val, src.ndarray, dst.ndarray, casting="unsafe")

        else:

            def cls_numpy_backend(self, src, val, dst):
                numpy_backend(src.ndarray, val, dst.ndarray, casting="unsafe")

        cls._numpy_backend = cls_numpy_backend

        def cls__call__(self, src, val, dst):
            assert (
                src.ndarray.size == dst.ndarray.size
            ), "src and dst size not compatible."

            numpy_ipps.status = self._ipps_backend(
                src.cdata, val, dst.cdata, dst.size
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
                (
                    "void*",
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    "void*",
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )

        return self


class BinaryC_I(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
        ipps_backend=None,
        numpy_backend=None,
        policies=numpy_ipps._detail.dispatch.keep_all,
        numpy_swap=False,
    ):
        attrs["__slots__"] = ("_ipps_backend",)
        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:
            attrs["__slots__"] = attrs["__slots__"] + ("_ipps_callback_64",)
        cls = super().__new__(mcs, name, bases, attrs)

        cls._ipps_backend_name = ipps_backend
        cls._ipps_policies = policies

        if policies.bytes8[0] in numpy_ipps._detail.dispatch.down_tags:

            def cls_ipps_backend_64(self, val, src_dst_cdata, src_dst_size):
                return self._ipps_callback_64(
                    val, src_dst_cdata, 2 * int(src_dst_size)
                )

            cls._ipps_backend_64 = cls_ipps_backend_64

        if numpy_swap:

            def cls_numpy_backend(self, val, src_dst):
                numpy_backend(
                    val, src_dst.ndarray, src_dst.ndarray, casting="unsafe"
                )

        else:

            def cls_numpy_backend(self, val, src_dst):
                numpy_backend(
                    src_dst.ndarray, val, src_dst.ndarray, casting="unsafe"
                )

        cls._numpy_backend = cls_numpy_backend

        def cls__call__(self, val, src_dst):
            numpy_ipps.status = self._ipps_backend(
                val, src_dst.cdata, src_dst.size
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
                (
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )
            self._ipps_backend = self._ipps_backend_64
        else:
            self._ipps_backend = numpy_ipps._detail.dispatch.ipps_function(
                cls._ipps_backend_name,
                (
                    numpy_ipps._detail.dispatch.as_ctype_str(
                        dtype, policies=cls._ipps_policies
                    ),
                    "void*",
                    "int",
                ),
                dtype,
                policies=cls._ipps_policies,
            )

        return self
