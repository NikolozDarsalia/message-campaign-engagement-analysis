import pandas as pd

def add_global_campaign_performance_features(df):
    """
    Adds global (company-level) engagement rate trends prior to each message.
    Calculates rolling open/click/purchase rates for the previous 1 day, 1 week, and 1 month.
    Uses 'closed=left' to avoid future leakage.
    """
    df = df.copy()
    df['sent_at'] = pd.to_datetime(df['sent_at'], errors='coerce')
    df = df.sort_values('sent_at')

    # Ensure boolean/0-1 metrics
    for col in ['is_opened', 'is_clicked', 'is_purchased']:
        df[col] = df[col].fillna(0).astype(int)

    # Set time index
    df_indexed = df.set_index('sent_at')

    # Aggregated message-level engagement metrics over time
    engagement_df = (
        df_indexed[['is_opened', 'is_clicked', 'is_purchased']]
        .resample('1H')
        .mean()
        .fillna(0)
    )

    # Compute rolling averages for 1 day, 1 week, 1 month (lookback windows)
    for period_label, window in [('1d', '1D'), ('1w', '7D'), ('1m', '30D')]:
        for metric in ['is_opened', 'is_clicked', 'is_purchased']:
            engagement_df[f'global_{metric}_rate_{period_label}'] = (
                engagement_df[metric].rolling(window=window, closed='left').mean()
            )

    # Merge back (asof merge ensures we only look backward in time)
    merge_cols = [
        f'global_is_opened_rate_1d', f'global_is_opened_rate_1w', f'global_is_opened_rate_1m',
        f'global_is_clicked_rate_1d', f'global_is_clicked_rate_1w', f'global_is_clicked_rate_1m',
        f'global_is_purchased_rate_1d', f'global_is_purchased_rate_1w', f'global_is_purchased_rate_1m'
    ]

    df = pd.merge_asof(
        df.sort_values('sent_at'),
        engagement_df[merge_cols].sort_index(),
        left_on='sent_at',
        right_index=True,
        direction='backward'
    )

    print("✅ Added global campaign performance trend features:")
    print(f"  - {', '.join(merge_cols)}")

    return df
