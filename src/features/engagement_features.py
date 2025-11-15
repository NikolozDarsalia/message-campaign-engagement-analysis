"""
Engagement and behavior-based features with anti-leakage design.
Includes lagged features, rolling rates, Bayesian smoothing, campaign quality, and expectation gaps.
"""

import pandas as pd
import numpy as np
from typing import List, Dict


def bayesian_shrinkage(successes, trials, global_mean, alpha=1, beta=1):
    """
    Apply Bayesian shrinkage smoothing to rates to handle low counts.
    
    Parameters
    ----------
    successes : array-like
        Cumulative number of successes
    trials : array-like
        Number of trials (observations)
    global_mean : float
        Global average rate
    alpha : float, default 1
        Prior strength parameter for successes
    beta : float, default 1
        Prior strength parameter for failures
        
    Returns
    -------
    array-like
        Smoothed rates
        
    Notes
    -----
    Formula: (successes + α*global_rate) / (trials + α + β)
    This shrinks estimates toward the global mean, especially for small samples.
    """
    return (successes + alpha * global_mean) / (trials + alpha + beta)


def create_lagged_engagement_features(
    df: pd.DataFrame, 
    verbose: bool = True
) -> pd.DataFrame:
    """
    Create lagged engagement indicators (shift by 1 to prevent leakage).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with engagement columns
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with lagged engagement features added
        
    Features Created
    ----------------
    - is_opened_prev, is_clicked_prev, is_purchased_prev
    - time_to_open_hours_prev, time_to_click_hours_prev
    """
    
    df = df.copy()
    
    if verbose:
        print("  Creating lagged engagement features...")
    
    # Engagement metrics to lag
    engagement_cols = ['is_opened', 'is_clicked', 'is_purchased']
    time_cols = ['time_to_open_hours', 'time_to_click_hours']
    
    features_created = 0
    
    # Lag engagement indicators
    for col in engagement_cols:
        if col in df.columns:
            df[f'{col}_prev'] = df.groupby('client_id')[col].shift(1)
            features_created += 1
    
    # Lag time-to-action features
    for col in time_cols:
        if col in df.columns:
            df[f'{col}_prev'] = df.groupby('client_id')[col].shift(1)
            features_created += 1
    
    if verbose:
        print(f"    ✅ Created {features_created} lagged features")
    
    return df


def create_rolling_engagement_rates(
    df: pd.DataFrame,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Create rolling engagement rates over time windows (anti-leakage design).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with lagged engagement features
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with rolling engagement rates added
        
    Features Created
    ----------------
    - is_opened_rate_1w, is_opened_rate_1m
    - is_clicked_rate_1w, is_clicked_rate_1m
    - is_purchased_rate_1w, is_purchased_rate_1m
    
    Notes
    -----
    Uses closed='left' to exclude current observation from rolling window.
    Computes rates from _prev columns to prevent target leakage.
    """
    
    df = df.copy()
    
    if verbose:
        print("  Creating rolling engagement rates...")
    
    engagement_metrics = ['is_opened', 'is_clicked', 'is_purchased']
    available_metrics = [m for m in engagement_metrics if m in df.columns]
    
    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df
    
    # Set index for rolling operations
    df_indexed = df.set_index('sent_at')
    
    features_created = 0
    
    for metric in available_metrics:
        prev_col = f'{metric}_prev'
        
        if prev_col not in df.columns:
            if verbose:
                print(f"    ⚠️  {prev_col} not found, skipping...")
            continue
        
        for period, days in [('1w', '7d'), ('1m', '30d')]:
            try:
                rolling_result = (
                    df_indexed.groupby('client_id', group_keys=False)[prev_col]
                    .rolling(days, closed='left')
                    .mean()
                )
                
                if isinstance(rolling_result.index, pd.MultiIndex):
                    rolling_result = rolling_result.reset_index(level=0, drop=True)
                
                df[f'{metric}_rate_{period}'] = rolling_result.values
                features_created += 1
                
            except Exception as e:
                if verbose:
                    print(f"    ⚠️  Could not compute {metric}_rate_{period}: {e}")
                df[f'{metric}_rate_{period}'] = np.nan
    
    if verbose:
        print(f"    ✅ Created {features_created} rolling rate features")
    
    return df


def create_bayesian_smoothed_rates(
    df: pd.DataFrame,
    alpha: float = 1,
    beta: float = 1,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Create Bayesian smoothed engagement rates (handles low-count clients).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with engagement columns
    alpha : float, default 1
        Prior strength for successes
    beta : float, default 1
        Prior strength for failures
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with smoothed rates added
        
    Features Created
    ----------------
    - is_opened_rate_prev_smooth
    - is_clicked_rate_prev_smooth
    - is_purchased_rate_prev_smooth
    
    Notes
    -----
    Uses cumulative sum shifted by 1 to prevent leakage.
    Shrinks rates toward global mean, especially for new clients.
    """
    
    df = df.copy()
    
    if verbose:
        print("  Creating Bayesian smoothed rates...")
    
    engagement_metrics = ['is_opened', 'is_clicked', 'is_purchased']
    available_metrics = [m for m in engagement_metrics if m in df.columns]
    
    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df
    
    global_rates = {}
    features_created = 0
    
    for metric in available_metrics:
        # Compute global rate
        global_rates[metric] = df[metric].mean()
        
        if verbose:
            print(f"    Global {metric} rate: {global_rates[metric]:.4f}")
        
        # Initialize column
        df[f'{metric}_rate_prev_smooth'] = np.nan
        
        # Compute smoothed rate per client
        for client_id, group_indices in df.groupby('client_id').groups.items():
            group = df.loc[group_indices]
            
            # Cumulative sum shifted by 1 (to avoid leakage)
            cumsum = group[metric].cumsum().shift(1).fillna(0).values
            trials = np.arange(len(group))
            
            # Apply Bayesian shrinkage
            smoothed = bayesian_shrinkage(
                successes=cumsum,
                trials=trials,
                global_mean=global_rates[metric],
                alpha=alpha,
                beta=beta
            )
            
            df.loc[group_indices, f'{metric}_rate_prev_smooth'] = smoothed
        
        features_created += 1
    
    if verbose:
        print(f"    ✅ Created {features_created} smoothed rate features")
    
    return df


def create_campaign_quality_features(
    df: pd.DataFrame,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Create campaign-level quality features (per-client, per-campaign history).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with campaign_id and engagement columns
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with campaign quality features added
        
    Features Created
    ----------------
    - is_opened_rate_campaign_per_client
    - is_clicked_rate_campaign_per_client
    - is_purchased_rate_campaign_per_client
    - is_purchased_rate_campaign
    - is_purchased_rate_campaign
    - is_purchased_rate_campaign
    
    Notes
    -----
    Computes expanding mean of engagement metrics per (client, campaign).
    Uses shift(1) to prevent leakage.
    """
    
    df = df.copy()
    
    if verbose:
        print("  Creating campaign quality features...")
    
    if 'campaign_id' not in df.columns:
        if verbose:
            print("    ⚠️  campaign_id not found, skipping...")
        return df
    
    engagement_metrics = ['is_opened', 'is_clicked', 'is_purchased']
    available_metrics = [m for m in engagement_metrics if m in df.columns]
    
    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df
    
    features_created = 0
    
    for metric in available_metrics:
        # Per-campaign historical performance for each client_id (excluding current message) 
        df[f'{metric}_rate_campaign_per_client'] = (
            df.groupby(['client_id', 'campaign_id'])[metric]
            .transform(lambda x: x.shift(1).expanding().mean())
        )
        features_created += 1

        # Per-campaign historical performance (excluding current message)
        df[f'{metric}_rate_campaign'] = (
            df.groupby(['campaign_id'])[metric]
            .transform(lambda x: x.shift(1).expanding().mean())
        )
        features_created += 1

    if verbose:
        print(f"    ✅ Created {features_created} campaign quality features")
    
    return df


def create_expectation_gap_features(
    df: pd.DataFrame,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Create expectation gap features (deviation from baseline behavior).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with rolling rates and smoothed rates
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with expectation gap features added
        
    Features Created
    ----------------
    For each metric (opened, clicked, purchased):
    - {metric}_expect_gap_1w: Recent (1w) vs smoothed baseline
    - {metric}_expect_gap_1m: Recent (1m) vs smoothed baseline
    - {metric}_expect_gap_overall: Overall avg vs smoothed baseline
    
    Notes
    -----
    Positive gap = performing better than baseline (potential revival)
    Negative gap = performing worse than baseline (potential fatigue)
    """
    
    df = df.copy()
    
    if verbose:
        print("  Creating expectation gap features...")
    
    engagement_metrics = ['is_opened', 'is_clicked', 'is_purchased']
    available_metrics = [m for m in engagement_metrics if m in df.columns]
    
    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df
    
    features_created = 0
    
    for metric in available_metrics:
        smooth_col = f'{metric}_rate_prev_smooth'
        
        if smooth_col not in df.columns:
            if verbose:
                print(f"    ⚠️  {smooth_col} not found, skipping gaps for {metric}")
            continue
        
        # Gap between recent rolling rates and smoothed historical rate
        for period in ['1w', '1m']:
            rate_col = f'{metric}_rate_{period}'
            
            if rate_col in df.columns:
                df[f'{metric}_expect_gap_{period}'] = (
                    df[rate_col] - df[smooth_col]
                )
                features_created += 1
        
        # Gap between overall client average and smoothed historical rate
        client_avg = df.groupby('client_id')[metric].transform('mean')
        df[f'{metric}_expect_gap_overall'] = client_avg - df[smooth_col]
        features_created += 1
    
    if verbose:
        print(f"    ✅ Created {features_created} expectation gap features")
    
    return df


def create_engagement_features(
    df: pd.DataFrame,
    bayesian_alpha: float = 1,
    bayesian_beta: float = 1,
    verbose: bool = True
) -> pd.DataFrame:
    """
    Create all engagement features (master orchestrator function).
    
    This function runs the complete engagement feature engineering pipeline:
    1. Lagged engagement indicators
    2. Rolling engagement rates (1w, 1m)
    3. Bayesian smoothed rates
    4. Campaign quality features
    5. Expectation gap features
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with basic features already created
    bayesian_alpha : float, default 1
        Prior strength for Bayesian smoothing (successes)
    bayesian_beta : float, default 1
        Prior strength for Bayesian smoothing (failures)
    verbose : bool, default True
        Print detailed progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with all engagement features added
        
    Examples
    --------
    >>> from src.features import create_engagement_features
    >>> df = create_engagement_features(df, verbose=True)
    
    Notes
    -----
    All features use anti-leakage design:
    - Lagged values (shift by 1)
    - Rolling windows with closed='left'
    - Expanding means with shift(1)
    
    This ensures features only use information available before prediction time.
    """
    
    df = df.copy()
    
    if verbose:
        print("\n" + "="*60)
        print("ENGAGEMENT FEATURE ENGINEERING")
        print("="*60)
        initial_cols = len(df.columns)
    
    # Check if engagement metrics exist
    engagement_metrics = ['is_opened', 'is_clicked', 'is_purchased']
    available_metrics = [m for m in engagement_metrics if m in df.columns]
    
    if not available_metrics:
        if verbose:
            print("⚠️  No engagement metrics (is_opened, is_clicked, is_purchased) found")
            print("Skipping engagement feature engineering")
        return df
    
    if verbose:
        print(f"Found {len(available_metrics)} engagement metrics: {', '.join(available_metrics)}")
        print()
    
    # Step 1: Lagged features
    df = create_lagged_engagement_features(df, verbose=verbose)
    
    # Step 2: Rolling rates
    df = create_rolling_engagement_rates(df, verbose=verbose)
    
    # Step 3: Bayesian smoothed rates
    df = create_bayesian_smoothed_rates(
        df, 
        alpha=bayesian_alpha, 
        beta=bayesian_beta, 
        verbose=verbose
    )
    
    # Step 4: Campaign quality
    df = create_campaign_quality_features(df, verbose=verbose)
    
    # Step 5: Expectation gaps
    df = create_expectation_gap_features(df, verbose=verbose)
    
    if verbose:
        final_cols = len(df.columns)
        new_features = final_cols - initial_cols
        
        print("\n" + "-"*60)
        print(f"SUMMARY: Created {new_features} engagement features")
        
        # Count by category
        categories = {
            'Lagged': len([c for c in df.columns if '_prev' in c]),
            'Rolling rates': len([c for c in df.columns if '_rate_1w' in c or '_rate_1m' in c]),
            'Smoothed rates': len([c for c in df.columns if 'rate_prev_smooth' in c]),
            'Campaign quality': len([c for c in df.columns if 'rate_campaign' in c]),
            'Expectation gaps': len([c for c in df.columns if 'expect_gap' in c])
        }
        
        for category, count in categories.items():
            if count > 0:
                print(f"  • {category}: {count}")
        
        print("="*60 + "\n")
    
    return df


def get_engagement_feature_list(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Get a categorized list of all engagement features in the dataframe.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with engagement features
        
    Returns
    -------
    dict
        Dictionary with feature categories as keys and lists of feature names as values
        
    Examples
    --------
    >>> features = get_engagement_feature_list(df)
    >>> print(f"Lagged features: {features['lagged']}")
    """
    
    return {
        'lagged': [c for c in df.columns if '_prev' in c],
        'rolling_rates': [c for c in df.columns if '_rate_1w' in c or '_rate_1m' in c],
        'smoothed_rates': [c for c in df.columns if 'rate_prev_smooth' in c],
        'campaign_quality': [c for c in df.columns if 'rate_campaign' in c],
        'expectation_gaps': [c for c in df.columns if 'expect_gap' in c],
        'all_engagement': [
            c for c in df.columns 
            if any(pattern in c for pattern in ['_prev', '_rate_', 'smooth', 'expect_gap', 'rate_campaign'])
        ]
    }