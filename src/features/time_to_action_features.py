import pandas as pd
import numpy as np


def add_lagged_avg_time_to_action(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Add lagged average time-to-open and time-to-click (no leakage):

    - avg_time_to_open_hours_prev
    - avg_time_to_click_hours_prev

    For each client and message:
    - avg_time_to_open_hours_prev = mean(time_to_open_hours) over all PREVIOUS messages of this client.
    - avg_time_to_click_hours_prev = mean(time_to_click_hours) over all PREVIOUS messages of this client.

    Current message's own time_to_* is excluded via shift.
    """
    df = df.copy()
    if verbose:
        print(
            "  Adding lagged avg_time_to_open_hours_prev and avg_time_to_click_hours_prev..."
        )

    if "client_id" not in df.columns or "sent_at" not in df.columns:
        if verbose:
            print("    ⚠️  client_id or sent_at not found, skipping.")
        return df

    df["sent_at"] = pd.to_datetime(df["sent_at"])
    df = df.sort_values(["client_id", "sent_at"])

    # Helper to compute cumulative mean excluding current row
    def cummean_excl_current(x: pd.Series) -> pd.Series:
        # shift to exclude current
        shifted = x.shift(1)
        cumsum = shifted.cumsum()
        counts = (~shifted.isna()).cumsum()
        return cumsum / counts

    if "time_to_open_hours" in df.columns:
        df["avg_time_to_open_hours_prev"] = df.groupby("client_id")[
            "time_to_open_hours"
        ].transform(cummean_excl_current)
    else:
        df["avg_time_to_open_hours_prev"] = np.nan

    if "time_to_click_hours" in df.columns:
        df["avg_time_to_click_hours_prev"] = df.groupby("client_id")[
            "time_to_click_hours"
        ].transform(cummean_excl_current)
    else:
        df["avg_time_to_click_hours_prev"] = np.nan

    if verbose:
        print(
            "    ✅ Added avg_time_to_open_hours_prev and avg_time_to_click_hours_prev"
        )

    return df
