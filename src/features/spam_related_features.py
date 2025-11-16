import pandas as pd

def create_spam_health_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create campaign deliverability and spam-related features.
    Expects df to have: ['client_id', 'sent_at', 'is_opened', 'is_clicked',
                         'is_purchased', 'is_soft_bounced', 'is_hard_bounced',
                         'is_blocked', 'is_unsubscribed', 'is_complained']
    """
    df = df.copy()
    df_indexed = df.set_index('sent_at')

    metrics = ['is_soft_bounced', 'is_hard_bounced', 'is_blocked', 'is_unsubscribed', 'is_complained']
    periods = {'1d': '1d', '1w': '7d', '1m': '30d'}

    print("Computing spam/delivery health features...")

    for metric in metrics:
        for label, window in periods.items():
            # Rolling per company (not per client)
            rolling_rate = (
                df_indexed[metric]
                .rolling(window=window, closed='left')
                .mean()
            )
            df[f'{metric}_rate_{label}'] = rolling_rate.values

    # Derived composite health metrics
    for label in ['1d', '1w', '1m']:
        df[f'delivery_rate_{label}'] = 1 - (
            df[f'is_soft_bounced_rate_{label}'].fillna(0)
            + df[f'is_hard_bounced_rate_{label}'].fillna(0)
        )
        df[f'spam_risk_index_{label}'] = (
            0.3 * df[f'is_soft_bounced_rate_{label}'].fillna(0)
            + 0.4 * df[f'is_hard_bounced_rate_{label}'].fillna(0)
            + 0.2 * df[f'is_blocked_rate_{label}'].fillna(0)
            + 0.05 * df[f'is_unsubscribed_rate_{label}'].fillna(0)
            + 0.05 * df[f'is_complained_rate_{label}'].fillna(0)
        )
    return df
