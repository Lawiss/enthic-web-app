import numpy as np
import pandas as pd
from numbers import Number


def format_numerical_value(value: Number, suffix: str = "") -> pd.Series:
    if not np.isnan(value):
        formated_value = f"{int(value):_d} {suffix}".replace("_", " ")

    return formated_value
