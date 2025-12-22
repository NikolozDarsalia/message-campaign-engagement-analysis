# 📊 Information Overload, Cognitive Capacity, and Customer Engagement

**Capstone Project Repository**

This repository contains the full data pipeline, feature engineering, modeling, interpretability analysis, and documentation for the capstone project:

> **Information Overload, Cognitive Capacity, and Customer Engagement: Evidence from Retail Messaging Data**

The project studies how messaging pressure, contextual cues, and customer heterogeneity shape engagement decisions (message openings) in high-frequency digital marketing environments.

---

## 📁 Repository Structure

```
capstone/
│
├── sampling/                  # Data reduction & construction
│   ├── Sampling.ipynb
│   ├── sampling_diagnostics.ipynb
│   └── combining_data.ipynb
│
├── nd_notebooks/              # Exploratory analysis
│   ├── healthCheck_EDA.ipynb
│   └── EDA_feature_engineering.ipynb
│
├── src/                       # Core Python code
│   ├── data_loading.py
│   ├── feature_engineering.py
│   ├── preprocess_for_fe.py
│   ├── counterfactuals_signal_design.py
│   ├── counterfactuals_coordination.py
│   └── features/
│       ├── engagement_features.py
│       ├── rolling_features.py
│       ├── market_features.py
│       ├── temporal_features.py
│       ├── spam_related_features.py
│       ├── holiday_features.py
│       ├── time_to_action_features.py
│       ├── global_campaign_performance_features.py
│       ├── clients_expectation_deviation_features.py
│       └── README.md
│
├── data/
│   └── README.md              # Description of original dataset fields
│
├── final_notebook.ipynb       # End-to-end analysis & results
├── Final_Paper.pdf            # Final academic report
├── pyproject.toml             # Dependencies & versions
├── LICENSE
└── README.md                  # This file
```

---

## 📦 Data Source

This project uses a publicly available anonymized marketing dataset hosted on Kaggle. The dataset contains email and push notification campaigns with delivery and open information.

**🔗 Kaggle Dataset:**  
[E-commerce multichannel direct messaging 2021-2023](https://www.kaggle.com/datasets/mkechinov/direct-messaging/data)

### ⚠️ Important Note

The original dataset contains **~721 million rows** and cannot be stored in this repository. Users must download it directly from Kaggle to reproduce the results.

---

## 🔍 Sampling Strategy (`/sampling`)

Due to the size of the raw dataset, we construct a manageable analytical sample:

- Randomly select ~55,000 customers
- Retain all messages sent to those customers
- Preserve within-customer histories and temporal structure

### Files

| File | Description |
|------|-------------|
| `Sampling.ipynb` | Performs client-level sampling using DuckDB |
| `sampling_diagnostics.ipynb` | Compares distributions (open rates, timing, message counts) before and after sampling to validate representativeness |
| `combining_data.ipynb` | Merges multiple Kaggle data files into a single analytical dataset after sampling |

This sampled dataset is used for all subsequent analysis: feature engineering, EDA, modeling, and counterfactuals.

---

## 🧪 Exploratory Analysis (`/nd_notebooks`)

Exploratory notebooks for initial analysis and feature validation:

| Notebook | Description |
|----------|-------------|
| `healthCheck_EDA.ipynb` | Basic sanity checks and descriptive statistics for original dataset features |
| `EDA_feature_engineering.ipynb` | Exploratory analysis of engineered features, including logistic regressions, GAMs, partial dependence plots, and statistical significance tests |

> **Note:** These notebooks are exploratory and not the final analysis.

---

## 🧠 Feature Engineering (`/src/features`)

Feature engineering is **modular** and **theory-driven**. Each file constructs features related to a specific economic mechanism.

### Feature Categories

- **Engagement history & belief proxies**
- **Rolling exposure and fatigue measures**
- **Market-level messaging pressure**
- **Temporal and calendar effects**
- **Spam-like patterns and attention signals**

### 📄 Detailed Documentation

A comprehensive explanation of every engineered feature is provided in:

**[`src/features/README.md`](src/features/README.md)**

The file `feature_engineering.py` integrates all feature modules into a unified pipeline.

> ℹ️ **Note:** Many engineered features are exploratory. Only a subset is used in the final model, but additional features are retained for further research or extensions.

---

## 🤖 Modeling & Interpretation

The main analysis is conducted in:

### 📓 [`final_notebook.ipynb`](final_notebook.ipynb)

This notebook includes:

#### 1. K-Means Clustering
- Customers segmented into **Loyal**, **Occasional**, and **Dormant** groups
- Based on prior belief and belief uncertainty proxies

#### 2. Predictive Model
- **Gradient-boosted trees (XGBoost)**
- Customer-level train/test split

#### 3. Interpretability
- **SHAP values**
- **Accumulated Local Effect (ALE) plots**
- **Partial dependence plots**
- All key plots computed by customer segment

#### 4. Counterfactual Simulations
- Signal design under fatigue
- Market-level coordination in messaging volume
- Implemented in dedicated Python modules

---

## 🔁 Counterfactual Modules

| Module | Description |
|--------|-------------|
| `counterfactuals_signal_design.py` | Simulates engagement under alternative subject line designs and fatigue levels |
| `counterfactuals_coordination.py` | Simulates coordinated vs. uncoordinated reductions in aggregate messaging pressure |

> **Note:** These counterfactuals are associational simulations, not causal interventions.

---

## 📄 Final Report

### 📘 [`Final_Paper.pdf`](Final_Paper.pdf)

The paper presents:

- Economic framework
- Testable predictions
- Empirical results
- ALE plots and counterfactual evidence
- Limitations and future directions

The paper was written alongside this codebase and reflects the final modeling choices.

---

## ⚙️ Reproducibility

All dependencies and versions are specified in:

**[`pyproject.toml`](pyproject.toml)**

### Installation

To reproduce the environment:

```bash
pip install -r pyproject.toml
```

Or using a modern Python package manager compatible with `pyproject.toml`.

---

## ⚠️ Important Notes

- **Results are associational, not causal**
- **Feature proxies are imperfect measures** of latent cognitive constructs
- **Counterfactuals illustrate model-implied trade-offs**, not policy guarantees

---

## 🚀 Extensions & Future Work

Potential directions for extending this research:

- Use additional engineered features for deeper heterogeneity analysis
- Estimate dynamic belief updating models
- Apply framework to alternative marketing datasets
- Explore causal designs with randomized messaging experiments

---

## 📜 License

This project is released under the **MIT License**.  
See [`LICENSE`](LICENSE) for details.

---

## 📧 Contact

For questions or collaboration inquiries, please open an issue in this repository.

---

## 🙏 Acknowledgments

- Dataset provided by [Kaggle](https://www.kaggle.com/datasets/mkechinov/ecommerce-events-history-in-cosmetics-shop)
- Built with Python, XGBoost, SHAP, and scikit-learn

---

**⭐ If you find this project useful, please consider giving it a star!**