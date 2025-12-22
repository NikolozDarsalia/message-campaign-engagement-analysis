import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def counterfactual_market_coordination(X_test, model, cluster_names):
    """
    ECONOMIC QUESTION:
    When market load is high, what happens if:
    (1) Everyone optimizes individually (Nash)
    (2) Industry coordinates to reduce total volume (Social optimum)
    """

    # ---------- SETUP ----------
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

    cluster_ids = sorted(cluster_names.keys())
    colors = ["#e74c3c", "#2ecc71", "#3498db"]

    # ---------- CHART 1: RESPONSE CURVES (TOP ROW - SPANS 2 COLUMNS) ----------
    ax1 = fig.add_subplot(gs[0, :2])

    your_volume_range = np.linspace(0, 20, 20)
    market_volume_scenarios = {
        "Current (High Load)": 200,
        "Coordinated (25% Reduction)": 150,
        "Coordinated (50% Reduction)": 100,
    }

    scenario_colors = ["#d62728", "#ff7f0e", "#2ca02c"]

    for idx, (market_label, market_vol) in enumerate(market_volume_scenarios.items()):
        cluster_responses = []

        for cluster_id in cluster_ids:
            X_cluster = X_test[X_test["cluster"] == cluster_id]
            X_features = X_cluster.drop(columns=["cluster"]).iloc[:3000]

            responses = []
            for your_vol in your_volume_range:
                X_cf = X_features.copy()
                X_cf["sent_count_1w"] = your_vol
                X_cf["market_avg_msgs_1m"] = market_vol
                pred = model.predict_proba(X_cf)[:, 1].mean()
                responses.append(pred)

            cluster_responses.append(responses)

        # Average across clusters
        avg_response = np.mean(cluster_responses, axis=0)

        linestyle = "-" if "Current" in market_label else "--"
        ax1.plot(
            your_volume_range,
            avg_response,
            linewidth=3.5,
            label=market_label,
            linestyle=linestyle,
            alpha=0.9,
            color=scenario_colors[idx],
        )

        # Mark optimal point
        opt_idx = np.argmax(avg_response)
        ax1.scatter(
            [your_volume_range[opt_idx]],
            [avg_response[opt_idx]],
            s=200,
            marker="*",
            edgecolors="black",
            linewidths=2,
            zorder=5,
            color=scenario_colors[idx],
        )

        # Annotate optimal point
        ax1.annotate(
            f"Optimal: {your_volume_range[opt_idx]:.1f}",
            xy=(your_volume_range[opt_idx], avg_response[opt_idx]),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=10,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.5",
                facecolor="white",
                edgecolor=scenario_colors[idx],
                linewidth=2,
            ),
        )

    ax1.set_xlabel("Your Message Volume (msgs/week)", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Average Open Rate", fontsize=13, fontweight="bold")
    ax1.set_title(
        "Individual Firm Response Under Different Market Conditions",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax1.legend(fontsize=11, loc="best", framealpha=0.95)
    ax1.grid(True, alpha=0.3)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # ---------- CHART 2: COORDINATION BENEFIT (TOP RIGHT) ----------
    ax2 = fig.add_subplot(gs[0, 2])

    # Calculate gains from coordination
    baseline_responses = []
    coord_50_responses = []
    coord_75_responses = []

    optimal_volume = 8  # Typical optimal from the curves

    for cluster_id in cluster_ids:
        X_cluster = X_test[X_test["cluster"] == cluster_id]
        X_features = X_cluster.drop(columns=["cluster"]).iloc[:2000]

        # Baseline
        X_cf = X_features.copy()
        X_cf["sent_count_1w"] = optimal_volume
        X_cf["market_avg_msgs_1m"] = 200
        baseline_responses.append(model.predict_proba(X_cf)[:, 1].mean())

        # 50% reduction
        X_cf = X_features.copy()
        X_cf["sent_count_1w"] = optimal_volume
        X_cf["market_avg_msgs_1m"] = 150
        coord_50_responses.append(model.predict_proba(X_cf)[:, 1].mean())

        # 75% reduction
        X_cf = X_features.copy()
        X_cf["sent_count_1w"] = optimal_volume
        X_cf["market_avg_msgs_1m"] = 100
        coord_75_responses.append(model.predict_proba(X_cf)[:, 1].mean())

    # Calculate percentage gains
    gains_50 = [
        (c50 - base) / base * 100
        for base, c50 in zip(baseline_responses, coord_50_responses)
    ]
    gains_75 = [
        (c75 - base) / base * 100
        for base, c75 in zip(baseline_responses, coord_75_responses)
    ]

    x = np.arange(len(cluster_ids))
    width = 0.35

    bars1 = ax2.bar(
        x - width / 2,
        gains_50,
        width,
        label="25% Reduction",
        color="#ff7f0e",
        alpha=0.8,
        edgecolor="black",
        linewidth=1.5,
    )
    bars2 = ax2.bar(
        x + width / 2,
        gains_75,
        width,
        label="50% Reduction",
        color="#2ca02c",
        alpha=0.8,
        edgecolor="black",
        linewidth=1.5,
    )

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.1f}%",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

    ax2.axhline(y=0, color="black", linestyle="-", linewidth=1)
    ax2.set_ylabel("Open Rate Lift (%)", fontsize=12, fontweight="bold")
    ax2.set_title(
        "Coordination Benefits\nby Customer Type",
        fontsize=13,
        fontweight="bold",
        pad=10,
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels([cluster_names[cid] for cid in cluster_ids], fontsize=11)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis="y")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    # ---------- POLICY SCENARIOS ----------
    policies = {
        "Status Quo": {"your_vol": 10, "market_vol": 200},
        "Self-Restraint Only (60%)": {"your_vol": 6, "market_vol": 200},
        "Market Cap (80%)": {"your_vol": 8, "market_vol": 160},
        "Market Cap (60%)": {"your_vol": 6, "market_vol": 120},
        "Aggressive Cap (40%)": {"your_vol": 4, "market_vol": 80},
    }

    policy_results = []

    for policy_name, params in policies.items():
        cluster_probs = []
        for cluster_id in cluster_ids:
            X_cluster = X_test[X_test["cluster"] == cluster_id]
            X_features = X_cluster.drop(columns=["cluster"]).iloc[:2000]

            X_cf = X_features.copy()
            X_cf["sent_count_1w"] = params["your_vol"]
            X_cf["market_avg_msgs_1m"] = params["market_vol"]
            pred = model.predict_proba(X_cf)[:, 1].mean()
            cluster_probs.append(pred)

        policy_results.append(
            {
                "policy": policy_name,
                "Dormant": cluster_probs[0],
                "Loyal": cluster_probs[1],
                "Occasional": cluster_probs[2],
                "Average": np.mean(cluster_probs),
            }
        )

    policy_df = pd.DataFrame(policy_results).set_index("policy")

    # ---------- CHART 3: POLICY HEATMAP (MIDDLE LEFT) ----------
    ax3 = fig.add_subplot(gs[1, :2])

    # Prepare data for heatmap
    heatmap_data = policy_df[["Dormant", "Loyal", "Occasional"]].values

    # Create heatmap
    im = ax3.imshow(
        heatmap_data,
        cmap="RdYlGn",
        aspect="auto",
        vmin=heatmap_data.min(),
        vmax=heatmap_data.max(),
    )

    # Set ticks and labels
    ax3.set_xticks(np.arange(3))
    ax3.set_yticks(np.arange(len(policies)))
    ax3.set_xticklabels(
        ["Dormant", "Loyal", "Occasional"], fontsize=11, fontweight="bold"
    )
    ax3.set_yticklabels(policy_df.index, fontsize=11)

    # Add text annotations
    for i in range(len(policies)):
        for j in range(3):
            text = ax3.text(
                j,
                i,
                f"{heatmap_data[i, j]:.4f}",
                ha="center",
                va="center",
                color="black",
                fontsize=11,
                fontweight="bold",
            )

    ax3.set_title(
        "Policy Scenario Comparison: Open Probability by Segment",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax3, orientation="vertical", pad=0.02)
    cbar.set_label("Open Probability", fontsize=11, fontweight="bold")

    # ---------- CHART 4: POLICY PERFORMANCE BARS (MIDDLE RIGHT) ----------
    ax4 = fig.add_subplot(gs[1, 2])

    # Sort policies by average performance
    policy_avg = policy_df["Average"].values
    policy_names_short = [
        "Status\nQuo",
        "Self-\nRestraint",
        "Cap\n80%",
        "Cap\n60%",
        "Cap\n40%",
    ]

    bars = ax4.barh(
        policy_names_short,
        policy_avg,
        color=["#d62728", "#ff7f0e", "#ffbb78", "#98df8a", "#2ca02c"],
        alpha=0.8,
        edgecolor="black",
        linewidth=1.5,
    )

    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax4.text(
            width,
            bar.get_y() + bar.get_height() / 2.0,
            f"{width:.4f}",
            ha="left",
            va="center",
            fontsize=10,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
        )

    ax4.set_xlabel("Average Open Probability", fontsize=12, fontweight="bold")
    ax4.set_title("Overall Policy Performance", fontsize=13, fontweight="bold", pad=10)
    ax4.grid(True, alpha=0.3, axis="x")
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    # ---------- CHART 5: LIFT FROM STATUS QUO (BOTTOM SPAN) ----------
    ax5 = fig.add_subplot(gs[2, :])

    # Calculate lift from status quo for each cluster
    status_quo_vals = policy_df.iloc[0][["Dormant", "Loyal", "Occasional"]].values

    lift_data = []
    for i in range(1, len(policy_df)):  # Skip status quo itself
        policy_vals = policy_df.iloc[i][["Dormant", "Loyal", "Occasional"]].values
        lifts = [(pv - sq) / sq * 100 for pv, sq in zip(policy_vals, status_quo_vals)]
        lift_data.append(lifts)

    lift_df = pd.DataFrame(
        lift_data, columns=["Dormant", "Loyal", "Occasional"], index=policy_df.index[1:]
    )

    # Create grouped bar chart
    x = np.arange(len(lift_df))
    width = 0.25

    for cluster_idx, cluster_label in enumerate(["Dormant", "Loyal", "Occasional"]):
        bars = ax5.bar(
            x + cluster_idx * width,
            lift_df[cluster_label],
            width,
            label=cluster_label,
            color=colors[cluster_idx],
            alpha=0.8,
            edgecolor="black",
            linewidth=1.5,
        )

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax5.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{height:.1f}%",
                ha="center",
                va="bottom" if height > 0 else "top",
                fontsize=9,
                fontweight="bold",
            )

    ax5.axhline(y=0, color="black", linestyle="-", linewidth=1.5)
    ax5.set_xlabel("Policy Scenario", fontsize=13, fontweight="bold")
    ax5.set_ylabel("Open Rate Lift from Status Quo (%)", fontsize=13, fontweight="bold")
    ax5.set_title(
        "Relative Performance: All Policies Beat Status Quo",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax5.set_xticks(x + width)
    ax5.set_xticklabels(lift_df.index, fontsize=11, rotation=15, ha="right")
    ax5.legend(fontsize=11, loc="best", framealpha=0.95)
    ax5.grid(True, alpha=0.3, axis="y")
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)

    # Add interpretation box
    textstr = "KEY INSIGHT: Market coordination benefits all segments"
    props = dict(
        boxstyle="round",
        facecolor="lightyellow",
        alpha=0.8,
        edgecolor="black",
        linewidth=2,
    )
    ax5.text(
        0.98,
        0.97,
        textstr,
        transform=ax5.transAxes,
        fontsize=11,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=props,
        fontweight="bold",
    )

    plt.suptitle(
        "COUNTERFACTUAL: Market Coordination vs. Individual Optimization\n"
        + "How Industry-Wide Volume Reduction Benefits All Stakeholders",
        fontsize=16,
        fontweight="bold",
        y=0.995,
    )

    plt.tight_layout()
    plt.show()

    return policy_df
