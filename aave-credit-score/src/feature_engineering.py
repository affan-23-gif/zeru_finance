import pandas as pd

def engineer_wallet_features(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)

    grouped = df.groupby('userWallet')

    features = []

    for wallet, group in grouped:
        wallet_data = {}
        wallet_data['userWallet'] = wallet
        wallet_data['num_actions'] = len(group)
        wallet_data['num_deposits'] = (group['action'] == 'deposit').sum()
        wallet_data['num_borrows'] = (group['action'] == 'borrow').sum()
        wallet_data['num_repays'] = (group['action'] == 'repay').sum()
        wallet_data['num_redeems'] = (group['action'] == 'redeemunderlying').sum()
        wallet_data['num_liquidations'] = (group['action'] == 'liquidationcall').sum()

        # Total and average amounts
        wallet_data['total_deposit'] = group[group['action'] == 'deposit']['amount'].sum()
        wallet_data['total_borrow'] = group[group['action'] == 'borrow']['amount'].sum()
        wallet_data['total_repay'] = group[group['action'] == 'repay']['amount'].sum()
        wallet_data['total_redeem'] = group[group['action'] == 'redeemunderlying']['amount'].sum()

        # Ratios
        wallet_data['repay_to_borrow_ratio'] = (
            wallet_data['total_repay'] / wallet_data['total_borrow']
            if wallet_data['total_borrow'] > 0 else 0
        )

        wallet_data['net_flow'] = (
            wallet_data['total_deposit'] - wallet_data['total_redeem']
        )

        # Time features
        active_days = group['timestamp'].dt.date.nunique()
        time_span = (group['timestamp'].max() - group['timestamp'].min()).days + 1
        wallet_data['active_days'] = active_days
        wallet_data['time_span_days'] = time_span

        # Asset diversity
        wallet_data['unique_assets_used'] = group['assetSymbol'].nunique()

        features.append(wallet_data)

    return pd.DataFrame(features)
