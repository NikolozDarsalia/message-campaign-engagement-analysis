import pandas as pd
import numpy as np

def add_client_vs_global_engagement_gap(df):
    """
    Adds features that compare client-level engagement behavior with global campaign engagement performance.

    For each metric (open, click, purchase) and each time window (1d, 1w, 1m):
      - Calculates (client_rate - global_rate) / global_rate
        -> Positive = client more engaged than market
        -> Negative = client less engaged than market

    Assumes client-level engagement rolling features and global engagement features already exist.
    """
    df = df.copy()

    # Define metrics and periods to compute deviations
    metrics = {
        'is_opened': 'open',
        'is_clicked': 'click',
        'is_purchased': 'purchase'
    }
    periods = ['1w', '1m']

    for metric_col, metric_short in metrics.items():
        for period in periods:
            client_col = f'{metric_col}_rate_{period}'  # from client rolling features
            global_col = f'global_{metric_col}_rate_{period}'  # from global features
            diff_col = f'{metric_short}_deviation_{period}'   # new feature name

            if client_col in df.columns and global_col in df.columns:
                # Compute relative deviation, safely handling division by zero
                df[diff_col] = (
                    (df[client_col] - df[global_col]) /
                    df[global_col].replace(0, np.nan)
                )
            else:
                print(f"⚠️ Missing columns for {metric_short} {period}: {client_col}, {global_col}")
                df[diff_col] = np.nan

    # Optionally replace infinities and fill extreme missing values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    print("✅ Added client vs. global engagement deviation features:")
    print("   - " + ", ".join([f"{m}_gap_{p}" for m in ['open','click','purchase'] for p in ['1d','1w','1m']]))

    return df
