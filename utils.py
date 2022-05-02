import numpy as np
import pandas as pd
from numbers import Number


def format_numerical_value(value: Number, suffix: str = "") -> str:
    """Pretty format a numerical value.

    Parameters
    ----------
    value : Number
        DataFrame including the variables needed to create the plot.
    suffix: str
        Optional suffix to add to the formated string, for example to add a unit.

    Returns
    -------
    str
        Number pretty formated as a string.
    """
    if not np.isnan(value):
        value = f"{int(value):_d} {suffix}".replace("_", " ")

    return value


def format_to_pretty_decimal(value: Number) -> str:
    """Pretty format a numerical value.

    Parameters
    ----------
    value : Number
        DataFrame including the variables needed to create the plot.
    Returns
    -------
    str
        Number pretty formated as a string.
    """
    return "{:,.2f}".format(float(value)).replace(",", " ")
