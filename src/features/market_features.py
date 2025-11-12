"""
Market-level and aggregate features.
"""

import pandas as pd


def create_market_features(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Create market-level aggregate features.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with other features
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with market features added
    """
    
    df = df.copy()
    
    if verbose:
        print("Creating market-level features...")
    
    # Aggregate by hour
    df_market = (
        df.groupby(pd.Grouper(key='sent_at', freq='1H'))
        .agg(total_msgs=('message_id', 'count'))
        .sort_index()
    )
    
    # Rolling averages at different time scales
    for lookback, suffix in [('6H', '6h'), ('1D', '1d'), ('7D', '1w'), ('30D', '1m')]:
        df_market[f'market_avg_msgs_{suffix}'] = (
            df_market['total_msgs']
            .rolling(lookback, closed='left')
            .mean()
        )
    
    # Merge back to main dataframe
    df = pd.merge_asof(
        df.sort_values('sent_at'),
        df_market,
        left_on='sent_at',
        right_index=True,
        direction='backward'
    )
    
    if verbose:
        print(f"  ✅ Created 5 market-level features")
    
    return df