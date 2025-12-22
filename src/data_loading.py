"""
Data loading
"""

import pandas as pd
from pathlib import Path
from typing import Union


def load_data(
    file_path: Union[str, Path],
    file_type: str = 'auto'
) -> pd.DataFrame:
    """
    Load data from various file formats with optional sampling.
    
    Parameters
    ----------
    file_path : str or Path
        Path to the data file
    file_type : str, default 'auto'
        File type: 'csv', 'parquet', 'auto'
        
    Returns
    -------
    pd.DataFrame
        Loaded dataframe
        
    """
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Auto-detect file type
    if file_type == 'auto':
        file_type = file_path.suffix.lower().replace('.', '')
    
    print(f"Loading data from {file_path}...")
    
    # Load based on file type
    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type == 'parquet':
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    print(f"✅ Loaded {len(df):,} rows, {len(df.columns)} columns")
    print(f"   Date range: {df['sent_at'].min() if 'sent_at' in df.columns else 'N/A'} to {df['sent_at'].max() if 'sent_at' in df.columns else 'N/A'}")
    
    return df

