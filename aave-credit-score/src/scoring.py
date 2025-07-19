import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def compute_credit_scores(features_df):
    df = features_df.copy()

    # Replace inf or NaN with 0 for safety
    df = df.fillna(0)
    df.replace([float('inf'), -float('inf')], 0, inplace=True)

    # Define feature weights (tune as needed)
    weights = {
        'repay_to_borrow_ratio': 0.25,
        'net_flow': 0.20,
        'unique_assets_used': 0.15,
        'active_days': 0.15,
        'time_span_days': 0.15,
        'num_liquidations': -0.10  # Negative weight = penalty
    }

    # Normalize features
    scaler = MinMaxScaler()
    for feature in weights:
        if weights[feature] >= 0:
            df[feature + "_scaled"] = scaler.fit_transform(df[[feature]])
        else:
            # Reverse scale for penalty features
            df[feature + "_scaled"] = 1 - scaler.fit_transform(df[[feature]])

    # Weighted score computation
    df['raw_score'] = sum(
        df[feature + "_scaled"] * abs(weight)
        for feature, weight in weights.items()
    )

    # Scale raw score to 0–1000
    df['credit_score'] = (df['raw_score'] - df['raw_score'].min()) / (
        df['raw_score'].max() - df['raw_score'].min()
    ) * 1000

    # Round and clean
    df['credit_score'] = df['credit_score'].round().astype(int)
    return df[['userWallet', 'credit_score']]
