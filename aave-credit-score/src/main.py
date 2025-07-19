from data_loader import load_transactions
from feature_engineering import engineer_wallet_features
from scoring import compute_credit_scores
import os

if __name__ == "__main__":
    json_path = os.path.join(os.path.dirname(__file__), "..", "data", "user-wallet-transactions.json")
    
    df_raw = load_transactions(json_path)
    df_wallet_features = engineer_wallet_features(df_raw)
    df_scores = compute_credit_scores(df_wallet_features)

    df_scores.to_csv("wallet_scores.csv", index=False)
    print(df_scores.head())
