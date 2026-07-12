"""Converts pandas/numpy values (including NA/NaN) into plain Python types
that pydantic schemas can serialize."""
import math

import numpy as np
import pandas as pd


def to_plain(value):
    if value is None:
        return None
    if value is pd.NA:
        return None
    if isinstance(value, np.ndarray):
        return [to_plain(v) for v in value.tolist()]
    if isinstance(value, list):
        return [to_plain(v) for v in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        v = float(value)
        return None if math.isnan(v) else v
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def records_from_df(df: pd.DataFrame) -> list[dict]:
    return [{k: to_plain(v) for k, v in record.items()} for record in df.to_dict("records")]
