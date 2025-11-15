"""
Main feature engineering orchestrator.
"""

import pandas as pd
from features.temporal_features import create_temporal_features
from features.rolling_features import create_rolling_features
from features.engagement_features import create_engagement_features
from features.market_features import create_market_features
from features.global_campaign_performance_features import add_global_campaign_performance_features
from features.clients_expectation_deviation_features import add_client_vs_global_engagement_gap
from features.spam_related_features import create_spam_health_features

def engineer_all_features(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Run complete feature engineering pipeline.
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned and prepared dataframe
    verbose : bool, default True
        Print progress messages
        
    Returns
    -------
    pd.DataFrame
        Dataframe with all engineered features
        
    Examples
    --------
    >>> from src import prepare_data, engineer_all_features
    >>> df = pd.read_csv('data/messages.csv')
    >>> df = prepare_data(df)
    >>> df = engineer_all_features(df)
    """
    
    if verbose:
        print("\n" + "="*60)
        print("FEATURE ENGINEERING PIPELINE")
        print("="*60)
        print(f"Input shape: {df.shape}\n")
    
    # Step 1: Temporal features
    df = create_temporal_features(df, verbose=verbose)
    
    # Step 2: Rolling features
    df = create_rolling_features(df, verbose=verbose)

    # Step 3: Market features
    df = create_market_features(df, verbose=verbose)

    # Remain only bulk messages
    df = df.loc[df['message_type'] == 'bulk', :].reset_index(drop=True)

    # Step 4: Engagement features
    df = create_engagement_features(df, verbose=verbose)

    
    # Step 5: Company level performance features
    df = add_global_campaign_performance_features(df)

    # Step 6: Client level engagement compare to overall engagement
    df = add_client_vs_global_engagement_gap(df)
    
    # Step 7: Detect temporary delivery issues and Potential Spam 
    df = create_spam_health_features(df)

    if verbose:
        print(f"\nFinal shape: {df.shape}")
        print(f"Total features created: {df.shape[1] - len(df.select_dtypes(include='object').columns)}")
        print("="*60 + "\n")
    
    return df


def engineer_message_features(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Engineer message and rolling features only (faster, no engagement).
    
    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with message features
    """
    
    if verbose:
        print("Engineering message features...")
    
    df = create_temporal_features(df, verbose=verbose)
    df = create_rolling_features(df, verbose=verbose)
    df = create_market_features(df, verbose=verbose)
    
    return df


def engineer_engagement_features(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Engineer engagement features only (requires message features first).
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with message features already created
    verbose : bool, default True
        Print progress
        
    Returns
    -------
    pd.DataFrame
        Dataframe with engagement features added
    """
    
    if verbose:
        print("Engineering engagement features...")
    
    df = create_engagement_features(df, verbose=verbose)
    
    return df