import numpy as np
import pandas as pd
from numbers import Number


def format_numerical_value(value: Number, suffix: str = "") -> pd.Series:
    if not np.isnan(value):
        value = f"{int(value):_d} {suffix}".replace("_", " ")

    return value


def format_to_pretty_decimal(value: Number) -> pd.Series:
    return "{:,.2f}".format(float(value)).replace(",", " ")
