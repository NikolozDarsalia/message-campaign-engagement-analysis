import pandas as pd
import numpy as np


def add_holiday_distance_features(
    df: pd.DataFrame,
    holidays_df: pd.DataFrame,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Add distance to the nearest past and future holiday (any holiday, any name).
    For each message at date:
    - If date IS a holiday: both distances = 0
    - Otherwise:
      - last_holiday_date = max holiday.date <= date
      - next_holiday_date = min holiday.date >= date
      - days_since_last_holiday = (date - last_holiday_date).days
      - days_until_next_holiday = (next_holiday_date - date).days

    Assumes:
    - df has column 'date' (datetime or convertible).
    - holidays_df has column 'date' (datetime or convertible).
    """
    df = df.copy()

    if verbose:
        print("  Adding holiday distance features (any holiday)...")

    # Ensure datetime
    df["date"] = pd.to_datetime(df["date"])
    holidays = holidays_df.copy()
    holidays["date"] = pd.to_datetime(holidays["date"])

    # Remove duplicate holiday dates (keep unique dates only)
    holidays = (
        holidays[["date"]].drop_duplicates().sort_values("date").reset_index(drop=True)
    )

    # Sort df
    df = df.sort_values("date").reset_index(drop=True)

    # Initialize columns
    df["days_since_last_holiday"] = np.nan
    df["days_until_next_holiday"] = np.nan

    # Get unique dates from df to avoid redundant calculations
    unique_dates = df["date"].unique()
    holiday_dates = holidays["date"].values
    holiday_set = set(pd.to_datetime(holiday_dates))

    # Create a mapping for each unique date
    date_to_last = {}
    date_to_next = {}

    for date in unique_dates:
        date_ts = pd.Timestamp(date)

        # Check if this date IS a holiday
        if date_ts in holiday_set:
            date_to_last[date] = 0
            date_to_next[date] = 0
        else:
            # Find last holiday (<=, so including same date if it were a holiday)
            past_holidays = holiday_dates[holiday_dates <= date]
            if len(past_holidays) > 0:
                last_holiday = past_holidays[-1]  # Most recent
                date_to_last[date] = (date_ts - pd.Timestamp(last_holiday)).days

            # Find next holiday (>=, so including same date if it were a holiday)
            future_holidays = holiday_dates[holiday_dates >= date]
            if len(future_holidays) > 0:
                next_holiday = future_holidays[0]  # Nearest future
                date_to_next[date] = (pd.Timestamp(next_holiday) - date_ts).days

    # Map back to df
    df["days_since_last_holiday"] = df["date"].map(date_to_last)
    df["days_until_next_holiday"] = df["date"].map(date_to_next)

    if verbose:
        print(
            "    ✅ Added days_since_last_holiday and days_until_next_holiday (any holiday)"
        )
        num_exact_matches = (df["days_since_last_holiday"] == 0).sum()
        print(f"    Found {num_exact_matches} dates that are holidays (distance = 0)")
        print(
            f"    Range days_since_last_holiday: {df['days_since_last_holiday'].min():.0f} to {df['days_since_last_holiday'].max():.0f}"
        )
        print(
            f"    Range days_until_next_holiday: {df['days_until_next_holiday'].min():.0f} to {df['days_until_next_holiday'].max():.0f}"
        )

    return df
