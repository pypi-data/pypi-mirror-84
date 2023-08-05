import json
import os

import numpy
import pylab


base_path = os.path.join(
    "log", "Linux-CPython-{}-64bit".format(os.environ["PYTHONVERSION"])
)
results = dict()
for counter in ["0001", "0002"]:
    try:
        with open(
            os.path.join(
                base_path,
                "{}_benchmark_py{}_{}.json".format(
                    counter,
                    os.environ["PYTHONVERSION"].replace(".", ""),
                    os.environ["PYTHONUPDATE"],
                ),
            )
        ) as json_file:
            for stats in json.load(json_file)["benchmarks"]:
                try:
                    pkg, fun = stats["name"].split("[", 1)[0].split("_")[1:]
                    ptype, porder = stats["param"].split("-")
                except BaseException:
                    continue
                if pkg not in results:
                    results[pkg] = dict()
                if fun not in results[pkg]:
                    results[pkg][fun] = dict()
                if ptype not in results[pkg][fun]:
                    results[pkg][fun][ptype] = dict()
                if porder not in results[pkg][fun][ptype]:
                    results[pkg][fun][ptype][porder] = stats["stats"]["ops"]
    except BaseException:
        continue

    if "numpy" in results:
        for fun in results["numpy"].keys():
            fig = pylab.figure(figsize=(8.25, 11.75))

            ax_ipps, ax_numpy, ax_relative = fig.subplots(3, 1)

            for ptype in results["ipps"][fun].keys():
                data_ipps = numpy.asarray(
                    [
                        [int(k), results["ipps"][fun][ptype][k]]
                        for k in results["ipps"][fun][ptype].keys()
                    ]
                )
                ax_ipps.loglog(
                    2 ** data_ipps[:, 0] * numpy.dtype(ptype).itemsize,
                    (2 ** data_ipps[:, 0])
                    * numpy.dtype(ptype).itemsize
                    * data_ipps[:, 1],
                    "o-.",
                    label=ptype,
                )
                data_numpy = numpy.asarray(
                    [
                        [int(k), results["numpy"][fun][ptype][k]]
                        for k in results["ipps"][fun][ptype].keys()
                    ]
                )
                ax_numpy.loglog(
                    2 ** data_numpy[:, 0] * numpy.dtype(ptype).itemsize,
                    (2 ** data_ipps[:, 0])
                    * numpy.dtype(ptype).itemsize
                    * data_numpy[:, 1],
                    "x-.",
                    label=ptype,
                )
                ax_relative.semilogx(
                    2 ** data_numpy[:, 0] * numpy.dtype(ptype).itemsize,
                    10 * numpy.log10(data_ipps[:, 1] / data_numpy[:, 1]),
                    "d-.",
                    label=ptype,
                )

            ax_numpy.legend(loc="upper right")
            ax_relative.set_xlabel("Memory (B)")

            ax_ipps.set_ylabel("Speed (B/s)")
            ax_numpy.set_ylabel("Speed (B/s)")
            ax_relative.set_ylabel("IPP vs Numpy Ratio (dB)")

            fig.savefig(
                os.path.join(base_path, "{}{}.svg".format(fun, counter))
            )
