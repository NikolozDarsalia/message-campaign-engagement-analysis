import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# ============================================================================
# COUNTERFACTUAL 1: OPTIMAL SIGNAL DESIGN UNDER DIFFERENT FATIGUE LEVELS
# "Bayesian Persuasion in a Fatigued Environment"
# ============================================================================


def counterfactual_signal_design_under_fatigue(X_test, model, cluster_names):
    """
    ECONOMIC QUESTION:
    When customers are fatigued (high message volume), what signal design
    maximizes opening probability? Should we use short+bonus or long+no bonus?

    This addresses Bayesian persuasion: optimal signal structure varies with
    receiver's cognitive state (attention capacity).
    """

    fig, axes = plt.subplots(1, 3, figsize=(20, 5))  # only one row now
    colors = ["#e74c3c", "#2ecc71", "#3498db"]
    cluster_ids = sorted(cluster_names.keys())

    # Define fatigue scenarios (message volume levels)
    fatigue_scenarios = {
        "Low Fatigue": {
            "bulk_count_1w": 1,
            "market_avg_msgs_1m": 100,
            "is_weekend": 1,
            "is_afternoon": 1,
            "global_is_opened_rate_1m": 0.15,
        },
        "Medium Fatigue": {
            "bulk_count_1w": 15,
            "market_avg_msgs_1m": 300,
            "is_weekend": 0,
            "is_afternoon": 1,
            "global_is_opened_rate_1m": 0.15,
        },
        "High Fatigue": {
            "bulk_count_1w": 40,
            "market_avg_msgs_1m": 6000,
            "is_weekend": 0,
            "is_afternoon": 0,
            "global_is_opened_rate_1m": 0.01,
        },
    }

    # Define signal design strategies
    subject_length_range = np.linspace(5, 250, 5)

    for col_idx, (scenario_name, fatigue_params) in enumerate(
        fatigue_scenarios.items()
    ):
        ax_top = axes[col_idx]

        for cluster_idx, cluster_id in enumerate(cluster_ids):
            X_cluster = X_test[X_test["cluster"] == cluster_id]
            X_features = X_cluster.drop(columns=["cluster"])

            cluster_label = cluster_names[cluster_id]

            # Strategy 1: With bonus
            probs_with_bonus = []
            for length in subject_length_range:
                X_cf = X_features.copy()
                X_cf["bulk_count_1w"] = fatigue_params["bulk_count_1w"]
                X_cf["market_avg_msgs_1m"] = fatigue_params["market_avg_msgs_1m"]
                X_cf["is_weekend"] = fatigue_params["is_weekend"]
                X_cf["is_afternoon"] = fatigue_params["is_afternoon"]
                X_cf["global_is_opened_rate_1m"] = fatigue_params[
                    "global_is_opened_rate_1m"
                ]
                X_cf["subject_length"] = length
                X_cf["subject_with_bonuses"] = 1
                pred = model.predict_proba(X_cf)[:, 1].mean()
                probs_with_bonus.append(pred)

            # Strategy 2: Without bonus
            probs_no_bonus = []
            for length in subject_length_range:
                X_cf = X_features.copy()
                X_cf["bulk_count_1w"] = fatigue_params["bulk_count_1w"]
                X_cf["market_avg_msgs_1m"] = fatigue_params["market_avg_msgs_1m"]
                X_cf["is_weekend"] = fatigue_params["is_weekend"]
                X_cf["is_afternoon"] = fatigue_params["is_afternoon"]
                X_cf["global_is_opened_rate_1m"] = fatigue_params[
                    "global_is_opened_rate_1m"
                ]
                X_cf["subject_length"] = length
                X_cf["subject_with_bonuses"] = 0
                pred = model.predict_proba(X_cf)[:, 1].mean()
                probs_no_bonus.append(pred)

            # Plot both strategies
            ax_top.plot(
                subject_length_range,
                probs_with_bonus,
                color=colors[cluster_idx],
                linewidth=2.5,
                label=f"{cluster_label} (w/ bonus)",
                alpha=0.9,
            )
            ax_top.plot(
                subject_length_range,
                probs_no_bonus,
                color=colors[cluster_idx],
                linewidth=2.5,
                linestyle="--",
                label=f"{cluster_label} (no bonus)",
                alpha=0.6,
            )

            # Mark optimal points
            opt_idx_bonus = np.argmax(probs_with_bonus)
            opt_idx_no = np.argmax(probs_no_bonus)
            ax_top.scatter(
                [subject_length_range[opt_idx_bonus]],
                [probs_with_bonus[opt_idx_bonus]],
                s=100,
                marker="*",
                color=colors[cluster_idx],
                edgecolors="black",
                linewidths=1.5,
                zorder=5,
            )

        ax_top.set_title(f"{scenario_name}", fontsize=12, fontweight="bold")
        ax_top.set_xlabel("Subject Length (chars)", fontsize=10)
        ax_top.set_ylabel("Open Probability", fontsize=10)
        ax_top.legend(fontsize=8, ncol=2, loc="best")
        ax_top.grid(True, alpha=0.3)

        # 🔑 Fix y-axis scale for comparability
        ax_top.set_ylim(0, 1)

    plt.suptitle(
        "COUNTERFACTUAL 1: Optimal Signal Design Under Different Fatigue Levels\n"
        + "Bayesian Persuasion in Attention-Constrained Environments",
        fontsize=15,
        fontweight="bold",
        y=0.995,
    )
    plt.tight_layout()
    plt.show()
