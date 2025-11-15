"""
Data preprocessing and cleaning utilities.
"""

import pandas as pd
import numpy as np

def prepare_data(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Prepare raw data for feature engineering.
    
    - Convert date columns to datetime
    - Remove duplicates
    - Sort by client and time
    - Basic data quality checks
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe
    verbose : bool, default True
        Print progress messages
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe ready for feature engineering
    """
    
    df = df.copy()
    
    if verbose:
        print("="*60)
        print("DATA PREPARATION")
        print("="*60)
        print(f"Initial shape: {df.shape}")
    
    # Convert datetime columns
    datetime_cols = ['sent_at', 'opened_first_time_at', 'opened_last_time_at',
                     'clicked_first_time_at', 'clicked_last_time_at',
                     'unsubscribed_at', 'hard_bounced_at', 'soft_bounced_at',
                     'complained_at', 'purchased_at', 'created_at', 'updated_at']
    
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Remove rows with invalid sent_at
    initial_count = len(df)
    df = df.dropna(subset=['sent_at'])
    
    if verbose and len(df) < initial_count:
        print(f"Removed {initial_count - len(df):,} rows with invalid sent_at")
    
    # Sort by client and time
    df = df.sort_values(['client_id', 'sent_at', 'message_id'])
    
    # Remove duplicate (client_id, sent_at) pairs
    initial_count = len(df)
    df = df.drop_duplicates(subset=['client_id', 'sent_at'], keep='first')
    
    if verbose and len(df) < initial_count:
        print(f"Removed {initial_count - len(df):,} duplicate timestamps")
    
    # Reset index
    df = df.reset_index(drop=True)
    
    if verbose:
        print(f"Final shape: {df.shape}")
        print(f"Date range: {df['sent_at'].min()} to {df['sent_at'].max()}")
        print(f"Unique clients: {df['client_id'].nunique():,}")
        print(f"Unique campaigns: {df['campaign_id'].nunique():,}")
        print("="*60 + "\n")
    
    return df


def clean_data(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Advanced data cleaning operations.
    
    - Handle outliers
    - Fix data quality issues
    - Create derived fields
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe after prepare_data()
    verbose : bool, default True
        Print progress messages
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe
    """
    
    df = df.copy()
    
    if verbose:
        print("Performing data cleaning...")
    
    # Cap time_to_open at reasonable maximum (e.g., 30 days)
    if 'opened_first_time_at' in df.columns:
        df['time_to_open_hours'] = (
            (df['opened_first_time_at'] - df['sent_at']).dt.total_seconds() / 3600
        )
        # Cap at 30 days = 720 hours
        df.loc[df['time_to_open_hours'] > 720, 'time_to_open_hours'] = np.nan
    
    # Similar for clicks
    if 'clicked_first_time_at' in df.columns:
        df['time_to_click_hours'] = (
            (df['clicked_first_time_at'] - df['sent_at']).dt.total_seconds() / 3600
        )
        df.loc[df['time_to_click_hours'] > 720, 'time_to_click_hours'] = np.nan
    
    # Ensure boolean columns are actually boolean
    bool_cols = ['is_opened', 'is_clicked', 'is_purchased', 'is_unsubscribed',
                 'is_hard_bounced', 'is_soft_bounced', 'is_complained', 'is_blocked']
    
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(bool)
    
    if verbose:
        print("✅ Data cleaning complete\n")
    
    return df