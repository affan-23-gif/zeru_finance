# 🏦 Aave V2 Wallet Credit Scoring

This project assigns a **credit score (0–1000)** to wallets on the Aave V2 protocol using historical transaction data. The scores are intended to reflect responsible usage, such as repaying borrowed assets, interacting across multiple assets, and avoiding liquidation.

---

## 🚀 Objective

Develop a pipeline that processes DeFi transaction logs and outputs a credit score per wallet, highlighting safe vs. risky users in a transparent, extensible manner.

---

## 📂 Project Structure

aave-credit-score/
├── data/
│ └── user-wallet-transactions.json
├── src/
│ ├── data_loader.py # Loads and flattens raw JSON
│ ├── feature_engineering.py # Aggregates user behavior metrics
│ ├── scoring.py # Normalizes + computes score (0–1000)
│ └── main.py # Main entry point to run pipeline
├── notebooks/
│ └── score_analysis.ipynb # Plots score distribution
├── wallet_scores.csv # Output scores
├── README.md
└── analysis.md # Score bin analysis



---

## 🛠️ Methodology

### Step 1: Load & Flatten JSON
The raw JSON file is parsed, and transaction fields (`userWallet`, `action`, `amount`, `timestamp`, etc.) are extracted.

### Step 2: Feature Engineering
Key wallet-level metrics are computed:
- Number of actions (`deposit`, `borrow`, etc.)
- Total and average transaction amounts
- Repay-to-borrow ratio
- Active time span
- Unique assets used
- Net flow (deposits - redeems)
- Liquidations (penalty)

### Step 3: Scoring Logic
A rule-based weighted scoring system was applied using the following formula:

\[
\text{score} = f(\text{repay ratio}, \text{net flow}, \text{diversity}, \text{time span}, \text{liquidation penalty})
\]

All features are normalized with `MinMaxScaler`, weighted, and mapped to a 0–1000 score.

---

## 🧪 Example Output

| userWallet                          | credit_score |
|------------------------------------|--------------|
| 0x0000000000001accf9...            | 730          |
| 0x000000000000e51b8e...            | 110          |

Run the full pipeline:
```bash
cd src
python main.py

