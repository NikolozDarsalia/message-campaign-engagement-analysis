"""
Rolling window features (counts, averages, ratios).
"""

import pandas as pd
import numpy as np


def create_rolling_features(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Create rolling window features using anti-leakage design (closed='left').
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with temporal features
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with rolling features added
    """
    
    df = df.copy()
    
    if verbose:
        print("Creating rolling features...")
    
    # Create binary indicators upfront
    df['is_email'] = (df['channel_x'] == 'email').astype(int) if 'channel_x' in df.columns else 0
    df['is_push'] = (df['channel_x'] == 'push').astype(int) if 'channel_x' in df.columns else 0
    
    if 'campaign_type' in df.columns:
        df['is_bulk'] = (df['campaign_type'] == 'bulk').astype(int)
        df['is_triggered'] = (df['campaign_type'] == 'triggered').astype(int)
        df['is_transactional'] = (df['campaign_type'] == 'transactional').astype(int)
    
        
    # Message position in campaign
    if 'campaign_id' in df.columns:
        df['msg_position_in_campaign'] = (
            df.groupby(['client_id', 'campaign_id']).cumcount() + 1
        )

    # Set index for rolling operations
    df_indexed = df.set_index('sent_at')
    
    # Rolling configuration
    rolling_configs = [
        # (column_name, output_prefix, aggregation_function, days, period_name)
        ('message_id', 'sent_count', 'count', '1d', '1d'),
        ('message_id', 'sent_count', 'count', '7d', '1w'),
        ('message_id', 'sent_count', 'count', '30d', '1m'),
        ('is_email', 'sent_count_email', 'sum', '1d', '1d'),
        ('is_email', 'sent_count_email', 'sum', '7d', '1w'),
        ('is_email', 'sent_count_email', 'sum', '30d', '1m'),
        ('is_push', 'sent_count_push', 'sum', '1d', '1d'),
        ('is_push', 'sent_count_push', 'sum', '7d', '1w'),
        ('is_push', 'sent_count_push', 'sum', '30d', '1m'),
        ('days_since_last_msg', 'avg_interval', 'mean', '1d', '1d'),
        ('days_since_last_msg', 'avg_interval', 'mean', '7d', '1w'),
        ('days_since_last_msg', 'avg_interval', 'mean', '30d', '1m'),
        ('is_weekend', 'weekend_ratio', 'mean', '7d', '1w'),
        ('is_weekend', 'weekend_ratio', 'mean', '30d', '1m'),
        ('is_working_hours', 'working_hours_ratio', 'mean', '1d', '1d'),
        ('is_working_hours', 'working_hours_ratio', 'mean', '7d', '1w'),
        ('is_working_hours', 'working_hours_ratio', 'mean', '30d', '1m'),
    ]
    
    # Add campaign type features if available
    if 'campaign_type' in df.columns:
        for ctype in ['bulk', 'triggered', 'transactional']:
            rolling_configs.extend([
                (f'is_{ctype}', f'{ctype}_count', 'sum', '1d', '1d'),
                (f'is_{ctype}', f'{ctype}_count', 'sum', '7d', '1w'),
                (f'is_{ctype}', f'{ctype}_count', 'sum', '30d', '1m'),
            ])
    
    # Add subject features if available
    if 'subject_length' in df.columns:
        rolling_configs.extend([
            ('subject_length', 'avg_subject_len', 'mean', '1d', '1d'),
            ('subject_length', 'avg_subject_len', 'mean', '7d', '1w'),
            ('subject_length', 'avg_subject_len', 'mean', '30d', '1m'),
        ])
    
        # Subject-specific features
    for feat in ['personalization', 'bonuses', 'saleout', 'discount', 'deadline', 'emoji']:
        col = f'subject_with_{feat}'
        if col in df.columns:
            rolling_configs.extend([
                (col, f'subject_{feat}_prop', 'mean', '1d', '1d'),
                (col, f'subject_{feat}_prop', 'mean', '7d', '1w'),
                (col, f'subject_{feat}_prop', 'mean', '30d', '1m'),
            ])
    
    # A/B test and warmup
    for mode_col in ['ab_test', 'warmup_mode']:
        if mode_col in df.columns:
            rolling_configs.extend([
                (mode_col, f'{mode_col}_count', 'sum', '1d', '1d'),
                (mode_col, f'{mode_col}_count', 'sum', '7d', '1w'),
                (mode_col, f'{mode_col}_count', 'sum', '30d', '1m'),
            ])
    

    # Compute all rolling features
    features_created = 0
    for col, prefix, agg_func, days, period in rolling_configs:
        if col not in df_indexed.columns:
            continue
        
        output_col = f'{prefix}_{period}'
        
        try:
            rolling_obj = df_indexed.groupby('client_id')[col].rolling(days, closed='left')
            
            if agg_func == 'count':
                result = rolling_obj.count()
            elif agg_func == 'sum':
                result = rolling_obj.sum()
            elif agg_func == 'mean':
                result = rolling_obj.mean()
            
            df[output_col] = result.reset_index(level=0, drop=True).values
            features_created += 1
            
        except Exception as e:
            if verbose:
                print(f"  Warning: Could not compute {output_col}: {e}")
            df[output_col] = np.nan
    
    # Unique campaigns
    if 'campaign_id' in df.columns:
        for days, period in [('1d', '1d'), ('7d', '1w'), ('30d', '1m')]:
            try:
                df[f'unique_campaigns_{period}'] = (
                    df_indexed.groupby('client_id')['campaign_id']
                    .rolling(days, closed='left')
                    .apply(lambda x: x.nunique(), raw=False)
                    .reset_index(level=0, drop=True)
                    .values
                )
                features_created += 1
            except:
                df[f'unique_campaigns_{period}'] = np.nan
    
    if verbose:
        print(f"  ✅ Created {features_created} rolling features")
    
    return df