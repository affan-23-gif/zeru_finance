import json
import pandas as pd

def load_transactions(json_path="../data/user-wallet-transactions.json"):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Flatten the nested structure
    records = []
    for entry in data:
        base = {
            'userWallet': entry.get('userWallet'),
            'network': entry.get('network'),
            'protocol': entry.get('protocol'),
            'txhash': entry.get('txhash'),
            'logId': entry.get('logId'),
            'timestamp': entry.get('timestamp'),
            'action': entry.get('action'),
        }
        action_data = entry.get('actionData', {})
        for key, value in action_data.items():
            base[key] = value
        records.append(base)

    df = pd.DataFrame(records)
    return df
