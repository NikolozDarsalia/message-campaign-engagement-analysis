"""
Temporal and time-based feature engineering.
"""

import pandas as pd
import numpy as np


def create_temporal_features(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Create temporal features from timestamps.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with sent_at column
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with temporal features added
    """
    
    df = df.copy()
    
    if verbose:
        print("Creating temporal features...")
    
    # Basic time components
    df['hour'] = df['sent_at'].dt.hour
    df['weekday'] = df['sent_at'].dt.weekday
    df['day_of_month'] = df['sent_at'].dt.day
    df['month'] = df['sent_at'].dt.month
    df['quarter'] = df['sent_at'].dt.quarter
    
    # Binary indicators
    df['is_weekend'] = (df['weekday'] >= 5).astype(int)
    df['is_working_hours'] = df['hour'].between(9, 18).astype(int)
    df['is_morning'] = df['hour'].between(6, 12).astype(int)
    df['is_afternoon'] = df['hour'].between(12, 18).astype(int)
    df['is_evening'] = df['hour'].between(18, 23).astype(int)
    df['is_night'] = ((df['hour'] >= 23) | (df['hour'] < 6)).astype(int)
    
    # Days since last message per client
    df['days_since_last_msg'] = (
        df.groupby('client_id')['sent_at']
        .diff()
        .dt.total_seconds()
        .div(86400)
    )
    
    # Days since last message by channel
    if 'channel_x' in df.columns:
        for ch in ['email', 'push']:
            df[f'days_since_last_{ch}'] = np.nan
            mask = df['channel_x'] == ch
            if mask.any():
                df.loc[mask, f'days_since_last_{ch}'] = (
                    df[mask].groupby('client_id')['sent_at']
                    .diff()
                    .dt.total_seconds()
                    .div(86400)
                    .values
                )
    
    if verbose:
        print(f"  ✅ Created {14 + (2 if 'channel_x' in df.columns else 0)} temporal features")
    
    return df