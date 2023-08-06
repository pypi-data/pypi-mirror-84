import json
import requests
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """

    def default(self, obj):
        if isinstance(
            obj,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {"real": obj.real, "imag": obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)):
            return None

        return json.JSONEncoder.default(self, obj)


def _infinite(scalar):
    """Creates an infinite generator from a scalar.

    Useful when zipping finite length iterators with single scalars.
    """
    while True:
        yield scalar


def _zipequalize(*iterables):
    """Creates equal length iterables for a mix of single and n-length arrays"""

    dims = set(map(len, iterables))
    if len(dims) == 1:
        return iterables

    if 1 not in dims or len(dims) > 2:
        raise ValueError("Input arrays dimensions mismatch.")

    out = []
    for it in iterables:
        if len(it) == 1:
            out.append(_infinite(it[0]))
        else:
            out.append(it)

    return out
