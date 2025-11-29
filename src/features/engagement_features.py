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
    """
    return (successes + alpha * global_mean) / (trials + alpha + beta)


def create_lagged_engagement_features(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create lagged engagement indicators (shift by 1 to prevent leakage).
    """
    df = df.copy()

    if verbose:
        print("  Creating lagged engagement features...")

    engagement_cols = ["is_opened", "is_clicked", "is_purchased"]
    time_cols = ["time_to_open_hours", "time_to_click_hours"]

    features_created = 0

    for col in engagement_cols:
        if col in df.columns:
            df[f"{col}_prev"] = df.groupby("client_id")[col].shift(1)
            features_created += 1

    for col in time_cols:
        if col in df.columns:
            df[f"{col}_prev"] = df.groupby("client_id")[col].shift(1)
            features_created += 1

    if verbose:
        print(f"    ✅ Created {features_created} lagged features")

    return df


def create_time_since_last_action_features(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create time since last opened / clicked / purchased (anti-leakage).

    Features created (in hours):
    - time_since_last_open_hours
    - time_since_last_click_hours
    - time_since_last_purchase_hours
    """
    df = df.copy()

    if verbose:
        print("  Creating time since last action features...")

    if "sent_at" not in df.columns:
        if verbose:
            print("    ⚠️  sent_at not found, skipping time since features...")
        return df

    # Ensure proper sorting and keep original index for alignment
    df = df.sort_values(["client_id", "sent_at"])
    original_index = df.index

    actions = {"open": "is_opened", "click": "is_clicked", "purchase": "is_purchased"}

    features_created = 0

    for action_name, col in actions.items():
        if col not in df.columns:
            continue

        # Build a Series of the last action time per row, using only this column
        # and preserving the DataFrame index.
        action_time = df["sent_at"].where(df[col] == 1, pd.NaT)

        # Forward-fill within client to get "last time this action happened up to now"
        last_action_time = action_time.groupby(df["client_id"]).ffill()

        # To avoid leakage, use the last action BEFORE current message:
        # shift the last_action_time series by 1 within each client.
        last_action_time_prev = last_action_time.groupby(df["client_id"]).shift(1)

        # Compute time difference in hours
        diff_hours = (df["sent_at"] - last_action_time_prev) / np.timedelta64(1, "h")
        df[f"time_since_last_{action_name}_hours"] = diff_hours

        features_created += 1

    # Restore original row order
    df = df.loc[original_index].sort_index()

    if verbose:
        print(f"    ✅ Created {features_created} time-since features")

    return df


def create_rolling_engagement_rates(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create rolling engagement rates over time windows (anti-leakage design).
    """
    df = df.copy()

    if verbose:
        print("  Creating rolling engagement rates...")

    engagement_metrics = ["is_opened", "is_clicked", "is_purchased"]
    available_metrics = [m for m in engagement_metrics if m in df.columns]

    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df

    df_indexed = df.set_index("sent_at")

    features_created = 0

    for metric in available_metrics:
        prev_col = f"{metric}_prev"

        if prev_col not in df.columns:
            if verbose:
                print(f"    ⚠️  {prev_col} not found, skipping...")
            continue

        for period, days in [("1w", "7d"), ("1m", "30d")]:
            try:
                rolling_result = (
                    df_indexed.groupby("client_id", group_keys=False)[prev_col]
                    .rolling(days, closed="left")
                    .mean()
                )

                if isinstance(rolling_result.index, pd.MultiIndex):
                    rolling_result = rolling_result.reset_index(level=0, drop=True)

                df[f"{metric}_rate_{period}"] = rolling_result.values
                features_created += 1

            except Exception as e:
                if verbose:
                    print(f"    ⚠️  Could not compute {metric}_rate_{period}: {e}")
                df[f"{metric}_rate_{period}"] = np.nan

    if verbose:
        print(f"    ✅ Created {features_created} rolling rate features")

    return df


def create_rolling_time_to_action_features(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create rolling average time-to-open and time-to-click (anti-leakage).

    Features created (window over past 30 days, excluding current row):
    - time_to_open_hours_avg_1m
    - time_to_click_hours_avg_1m
    """
    df = df.copy()

    if verbose:
        print("  Creating rolling time-to-action averages...")

    if "sent_at" not in df.columns:
        if verbose:
            print("    ⚠️  sent_at not found, skipping rolling time features...")
        return df

    time_cols = ["time_to_open_hours", "time_to_click_hours"]
    available_time_cols = [c for c in time_cols if c in df.columns]

    if not available_time_cols:
        if verbose:
            print("    ⚠️  No time-to-action metrics found")
        return df

    df_indexed = df.set_index("sent_at")
    features_created = 0

    for col in available_time_cols:
        try:
            rolling_result = (
                df_indexed.groupby("client_id", group_keys=False)[col]
                .rolling("30d", closed="left")
                .mean()
            )

            if isinstance(rolling_result.index, pd.MultiIndex):
                rolling_result = rolling_result.reset_index(level=0, drop=True)

            df[f"{col}_avg_1m"] = rolling_result.values
            features_created += 1

        except Exception as e:
            if verbose:
                print(f"    ⚠️  Could not compute rolling avg for {col}: {e}")
            df[f"{col}_avg_1m"] = np.nan

    if verbose:
        print(f"    ✅ Created {features_created} rolling time-to-action features")

    return df


def create_bayesian_smoothed_rates(
    df: pd.DataFrame, alpha: float = 1, beta: float = 1, verbose: bool = True
) -> pd.DataFrame:
    """
    Create Bayesian smoothed engagement rates (handles low-count clients).
    """
    df = df.copy()

    if verbose:
        print("  Creating Bayesian smoothed rates...")

    engagement_metrics = ["is_opened", "is_clicked", "is_purchased"]
    available_metrics = [m for m in engagement_metrics if m in df.columns]

    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df

    global_rates = {}
    features_created = 0

    for metric in available_metrics:
        global_rates[metric] = df[metric].mean()

        if verbose:
            print(f"    Global {metric} rate: {global_rates[metric]:.4f}")

        df[f"{metric}_rate_prev_smooth"] = np.nan

        for client_id, group_indices in df.groupby("client_id").groups.items():
            group = df.loc[group_indices]

            cumsum = group[metric].cumsum().shift(1).fillna(0).values
            trials = np.arange(len(group))

            smoothed = bayesian_shrinkage(
                successes=cumsum,
                trials=trials,
                global_mean=global_rates[metric],
                alpha=alpha,
                beta=beta,
            )

            df.loc[group_indices, f"{metric}_rate_prev_smooth"] = smoothed

        features_created += 1

    if verbose:
        print(f"    ✅ Created {features_created} smoothed rate features")

    return df


def create_campaign_quality_features(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create campaign-level quality features (per-client, per-campaign history).
    """
    df = df.copy()

    if verbose:
        print("  Creating campaign quality features...")

    if "campaign_id" not in df.columns:
        if verbose:
            print("    ⚠️  campaign_id not found, skipping...")
        return df

    engagement_metrics = ["is_opened", "is_clicked", "is_purchased"]
    available_metrics = [m for m in engagement_metrics if m in df.columns]

    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df

    features_created = 0

    for metric in available_metrics:
        df[f"{metric}_rate_campaign_per_client"] = df.groupby(
            ["client_id", "campaign_id"]
        )[metric].transform(lambda x: x.shift(1).expanding().mean())
        features_created += 1

        df[f"{metric}_rate_campaign"] = df.groupby(["campaign_id"])[metric].transform(
            lambda x: x.shift(1).expanding().mean()
        )
        features_created += 1

    if verbose:
        print(f"    ✅ Created {features_created} campaign quality features")

    return df


def create_expectation_gap_features(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create expectation gap features (deviation from baseline behavior).
    """
    df = df.copy()

    if verbose:
        print("  Creating expectation gap features...")

    engagement_metrics = ["is_opened", "is_clicked", "is_purchased"]
    available_metrics = [m for m in engagement_metrics if m in df.columns]

    if not available_metrics:
        if verbose:
            print("    ⚠️  No engagement metrics found")
        return df

    features_created = 0

    for metric in available_metrics:
        smooth_col = f"{metric}_rate_prev_smooth"

        if smooth_col not in df.columns:
            if verbose:
                print(f"    ⚠️  {smooth_col} not found, skipping gaps for {metric}")
            continue

        for period in ["1w", "1m"]:
            rate_col = f"{metric}_rate_{period}"

            if rate_col in df.columns:
                df[f"{metric}_expect_gap_{period}"] = df[rate_col] - df[smooth_col]
                features_created += 1

        client_avg = df.groupby("client_id")[metric].transform("mean")
        df[f"{metric}_expect_gap_overall"] = client_avg - df[smooth_col]
        features_created += 1

    if verbose:
        print(f"    ✅ Created {features_created} expectation gap features")

    return df


def create_open_rate_prior_variance_feature(
    df: pd.DataFrame,
    verbose: bool = True,
    window_days: int = 14,
    max_windows: int = None,
    penalty_lambda: float = 1.0,
) -> pd.DataFrame:
    """
    For each client and each message, compute:
    - Variance of past non-overlapping 14-day open rates (before current sent_at)
    - Penalized variance based on that variance and number of windows

    For a message at time t:
    - Consider windows (t-14, t], (t-28, t-14], (t-42, t-28], ...,
      implemented as [t-k*14d, t-(k-1)*14d), with strict < t.
    - Only use windows fully before t.
    - In each window, compute open rate if there is at least 1 message.
    - var = variance of these window open rates (if >= 2 windows, else NaN).
    - n_windows = number of windows with messages.
    - weight = (n_windows + penalty_lambda) / n_windows
    - variance = variance * weight

    Features:
    - open_rate_14d_prior_var
    """
    df = df.copy()

    if verbose:
        print("  Creating non-overlapping 14-day prior variance of open rates...")

    if "sent_at" not in df.columns or "is_opened" not in df.columns:
        if verbose:
            print("    ⚠️  sent_at or is_opened not found, skipping feature...")
        return df

    df = df.sort_values(["client_id", "sent_at"])
    original_index = df.index

    window_delta = pd.Timedelta(days=window_days)

    def per_client_prior_stats(client_df: pd.DataFrame) -> pd.DataFrame:
        client_df = client_df.sort_values("sent_at").copy()
        times = client_df["sent_at"].values
        opens = client_df["is_opened"].values
        n = len(client_df)

        prior_var = np.full(n, np.nan, dtype=float)

        for i in range(n):
            t = times[i]

            window_rates = []
            start = t - window_delta
            end = t

            window_count = 0
            while True:
                in_window = (times < end) & (times >= start)
                if in_window.any():
                    window_opens = opens[in_window]
                    window_rates.append(window_opens.mean())

                window_count += 1
                if max_windows is not None and window_count >= max_windows:
                    break

                end = start
                start = end - window_delta

                if end <= times[0]:
                    break

            n_windows = len(window_rates)

            if n_windows >= 2:
                arr = np.array(window_rates, dtype=float)
                var = arr.var(ddof=0)

                # penalized variance
                weight = (n_windows + penalty_lambda) / n_windows
                var = var * weight

                prior_var[i] = var
            else:
                prior_var[i] = np.nan

        result = pd.DataFrame(
            {"open_rate_14d_prior_var": prior_var},
            index=client_df.index,
        )
        return result

    stats = df.groupby("client_id", group_keys=False).apply(per_client_prior_stats)

    df = df.join(stats)

    df = df.loc[original_index].sort_index()

    if verbose:
        print("    ✅ Created open_rate_14d_prior_var")

    return df


def create_open_click_count_window_features(
    df: pd.DataFrame, verbose: bool = True
) -> pd.DataFrame:
    """
    Create counts of opened and clicked messages over 1w and 1m,
    plus '1m except 1w' (month minus week).

    Features:
    - opened_count_1w, opened_count_1m, opened_count_1m_ex_1w
    - clicked_count_1w, clicked_count_1m, clicked_count_1m_ex_1w
    - purchased_count_1w, purchased_count_1m, purchased_count_1m_ex_1w
    """
    df = df.copy()

    if verbose:
        print("  Creating open/click count window features...")

    if "sent_at" not in df.columns:
        if verbose:
            print("    ⚠️  sent_at not found, skipping count window features...")
        return df

    df_indexed = df.set_index("sent_at")

    events = {
        "opened": "is_opened",
        "clicked": "is_clicked",
        "purchased": "is_purchased",
    }

    features_created = 0

    for name, col in events.items():
        if col not in df.columns:
            continue

        # Use closed='left' to exclude current row
        for period, window in [("1w", "7d"), ("1m", "30d")]:
            try:
                rolling_count = (
                    df_indexed.groupby("client_id", group_keys=False)[col]
                    .rolling(window, closed="left")
                    .sum()
                )

                if isinstance(rolling_count.index, pd.MultiIndex):
                    rolling_count = rolling_count.reset_index(level=0, drop=True)

                df[f"{name}_count_{period}"] = rolling_count.values
                features_created += 1

            except Exception as e:
                if verbose:
                    print(f"    ⚠️  Could not compute {name}_count_{period}: {e}")
                df[f"{name}_count_{period}"] = np.nan

        # month except week = 1m - 1w
        if f"{name}_count_1m" in df.columns and f"{name}_count_1w" in df.columns:
            df[f"{name}_count_1m_ex_1w"] = (
                df[f"{name}_count_1m"] - df[f"{name}_count_1w"]
            )
            features_created += 1

    if verbose:
        print(f"    ✅ Created {features_created} open/click count window features")

    return df


def create_engagement_features(
    df: pd.DataFrame,
    bayesian_alpha: float = 1,
    bayesian_beta: float = 1,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Create all engagement features (master orchestrator function).
    """
    df = df.copy()

    if verbose:
        print("\n" + "=" * 60)
        print("ENGAGEMENT FEATURE ENGINEERING")
        print("=" * 60)
        initial_cols = len(df.columns)

    engagement_metrics = ["is_opened", "is_clicked", "is_purchased"]
    available_metrics = [m for m in engagement_metrics if m in df.columns]

    if not available_metrics:
        if verbose:
            print(
                "⚠️  No engagement metrics (is_opened, is_clicked, is_purchased) found"
            )
            print("Skipping engagement feature engineering")
        return df

    if verbose:
        print(
            f"Found {len(available_metrics)} engagement metrics: {', '.join(available_metrics)}"
        )
        print()

    # Step 0: sort by client and time to ensure consistency
    if "sent_at" in df.columns:
        df = df.sort_values(["client_id", "sent_at"])

    # Step 1: Lagged features
    df = create_lagged_engagement_features(df, verbose=verbose)

    # Step 1b: Time since last actions
    df = create_time_since_last_action_features(df, verbose=verbose)

    # Step 2: Rolling rates
    df = create_rolling_engagement_rates(df, verbose=verbose)

    # Step 2b: Rolling average time-to-open/click
    df = create_rolling_time_to_action_features(df, verbose=verbose)

    # Step 3: Bayesian smoothed rates
    df = create_bayesian_smoothed_rates(
        df, alpha=bayesian_alpha, beta=bayesian_beta, verbose=verbose
    )

    # Step 4: Campaign quality
    df = create_campaign_quality_features(df, verbose=verbose)

    # Step 5: Expectation gaps
    df = create_expectation_gap_features(df, verbose=verbose)

    # Step 6: 14-day interval open-rate variance (stability)
    df = create_open_rate_prior_variance_feature(df, verbose=verbose)

    # Step 7: Open/click counts in 1w / 1m / 1m_ex_1w
    df = create_open_click_count_window_features(df, verbose=verbose)

    if verbose:
        final_cols = len(df.columns)
        new_features = final_cols - initial_cols

        print("\n" + "-" * 60)
        print(f"SUMMARY: Created {new_features} engagement features")

        categories = {
            "Lagged": len([c for c in df.columns if "_prev" in c]),
            "Rolling rates": len(
                [c for c in df.columns if "_rate_1w" in c or "_rate_1m" in c]
            ),
            "Smoothed rates": len([c for c in df.columns if "rate_prev_smooth" in c]),
            "Campaign quality": len([c for c in df.columns if "rate_campaign" in c]),
            "Expectation gaps": len([c for c in df.columns if "expect_gap" in c]),
            "Time since actions": len(
                [c for c in df.columns if "time_since_last_" in c]
            ),
            "Rolling time-to-action": len(
                [c for c in df.columns if "_avg_1m" in c and "time_to_" in c]
            ),
            "14d open rate variance": len(
                [c for c in df.columns if "open_rate_14d_interval_variance" in c]
            ),
            "Open/click counts": len(
                [c for c in df.columns if "_count_1w" in c or "_count_1m" in c]
            ),
        }

        for category, count in categories.items():
            if count > 0:
                print(f"  • {category}: {count}")

        print("=" * 60 + "\n")

    return df


def get_engagement_feature_list(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Get a categorized list of all engagement features in the dataframe.
    """
    return {
        "lagged": [c for c in df.columns if "_prev" in c],
        "rolling_rates": [c for c in df.columns if "_rate_1w" in c or "_rate_1m" in c],
        "smoothed_rates": [c for c in df.columns if "rate_prev_smooth" in c],
        "campaign_quality": [c for c in df.columns if "rate_campaign" in c],
        "expectation_gaps": [c for c in df.columns if "expect_gap" in c],
        "time_since_actions": [c for c in df.columns if "time_since_last_" in c],
        "rolling_time_to_action": [
            c for c in df.columns if "_avg_1m" in c and "time_to_" in c
        ],
        "open_rate_14d_variance": [
            c for c in df.columns if "open_rate_14d_interval_variance" in c
        ],
        "open_click_counts": [
            c for c in df.columns if "_count_1w" in c or "_count_1m" in c
        ],
        "all_engagement": [
            c
            for c in df.columns
            if any(
                pattern in c
                for pattern in [
                    "_prev",
                    "_rate_",
                    "smooth",
                    "expect_gap",
                    "rate_campaign",
                    "time_since_last_",
                    "_avg_1m",
                    "_count_1w",
                    "_count_1m",
                    "open_rate_14d_interval_variance",
                ]
            )
        ],
    }
