import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class FatigueImputer(BaseEstimator, TransformerMixin):
    """
    Custom imputation pipeline for message-level fatigue dataset.
    
    Handles:
        - structural missing values
        - cold-start missing values
        - timestamp-derived features
        - categorical imputation
        - dropping useless columns
    """

    def __init__(self, drop_cold_start=True):
        self.drop_cold_start = drop_cold_start
        self.columns_to_drop = [
            "category", "platform", "is_test", "position",
            "blocked_at", "days_since_last_trigger",
              "days_since_last_transactional",
            ""  # all 100% null
        ]
        self.categorical_fill_value = "unknown"

    def fit(self, X, y=None):
        return self

    def transform(self, df):
        df = df.copy()

        # -------------------------------------------------------------
        # 1. DROP USELESS COLUMNS (100% null)
        # -------------------------------------------------------------
        for col in self.columns_to_drop:
            if col in df.columns:
                df.drop(columns=[col], inplace=True, errors="ignore")

        # -------------------------------------------------------------
        # 2. HANDLE CATEGORICAL COLUMNS
        # -------------------------------------------------------------
        categorical_cols = ["email_provider", "topic", "ab_test"]
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].fillna(self.categorical_fill_value)

        # -------------------------------------------------------------
        # 3. HANDLE EVENT FLAGS AND TIME-TO-EVENT FEATURES
        # -------------------------------------------------------------
        binary_event_flags = [
            "is_opened_prev", "is_clicked_prev", "is_purchased_prev"
        ]
        for col in binary_event_flags:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(int)

        time_features = [
            "time_to_open_hours", "time_to_click_hours",
            "time_to_open_hours_prev", "time_to_click_hours_prev"
        ]
        for col in time_features:
            if col in df.columns:
                df[col] = df[col].fillna(0)

        # -------------------------------------------------------------
        # 4. HANDLE WINDOW FEATURES (1d, 1w, 1m)
        #    cold start → 0 or drop rows
        # -------------------------------------------------------------
        window_prefixes = [
            "sent_count", "avg_interval", "weekend_ratio", "working_hours_ratio",
            "bulk_count", "triggered_count", "transactional_count",
            "avg_subject_len", "subject_personalization_prop",
            "subject_bonuses_prop", "subject_saleout_prop",
            "subject_discount_prop", "subject_deadline_prop",
            "subject_emoji_prop", "ab_test_count", "warmup_mode_count",
            "unique_campaigns", "is_opened_rate", "is_clicked_rate",
            "is_purchased_rate", "open_deviation", "click_deviation",
            "purchase_deviation"
        ]

        window_cols = [c for c in df.columns 
                       if any(c.startswith(prefix) for prefix in window_prefixes)]

        if self.drop_cold_start:
            # Drop rows where ALL window features are missing
            df = df[~df[window_cols].isna().all(axis=1)]
        else:
            # Fill cold-start nulls with 0
            df[window_cols] = df[window_cols].fillna(0)

        # -------------------------------------------------------------
        # 5. GLOBAL RATE FEATURES (rare nulls → ff + fill 0)
        # -------------------------------------------------------------
        global_cols = [c for c in df.columns if c.startswith("global")]
        df[global_cols] = df[global_cols].fillna(method="ffill").fillna(0)

        # -------------------------------------------------------------
        # 6. MISSING INDICATORS (optional)
        # -------------------------------------------------------------
        # You may add indicators if needed for ML interpretability.
        # Example:
        # df["missing_sent_count_1w"] = df["sent_count_1w"].isna().astype(int)

        return df
