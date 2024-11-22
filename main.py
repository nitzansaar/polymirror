import requests
from datetime import datetime
import json

# Top dog addresses
addresses = [
    "0x56687bf447db6ffa42ffe2204a05edaa20f55839", 
    "0x1f2dd6d473f3e824cd2f8a89d9c69fb96f6ad0cf", 
    "0x78b9ac44a6d7d7a076c14e0ad518b301b63c6b76"
]

# Define API endpoint and parameters for NFT transactions
url = "https://api.polygonscan.com/api"
params = {
    "module": "account",
    "action": "tokennfttx",  # NFT transactions, includes both ERC-721 and ERC-1155
    "address": addresses[0],  # Use the first address from the list
    "startblock": 0,
    "endblock": 99999999,
    "page": 1,
    "offset": 100,  # Adjust to fetch more transactions per page
    "sort": "desc",  # Fetch the most recent transactions first
    "apikey": "QWBM6IIDNGC3GX5ZPJD4PFEZB1X7YSJ4EB",  # Replace with your actual API key
}

# Fetch NFT transactions
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if data["status"] == "1":  # API response success
        transactions = data["result"]

        # Filter for ERC-1155 tokens
        erc1155_transactions = []
        for tx in transactions:
            # Filter ERC-1155 tokens based on quantity (value > 1 indicates ERC-1155)
            if int(tx.get("value", "1")) > 1:  # ERC-721 tokens usually have value = 1
                timestamp = datetime.fromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S')
                
                tx_data = {
                    "transaction_hash": tx["hash"],
                    "from": tx["from"],
                    "to": tx["to"],
                    "token_id": tx["tokenID"],  # Token ID for ERC-1155
                    "amount": tx["value"],  # Quantity transferred
                    "timestamp": timestamp,
                }
                erc1155_transactions.append(tx_data)

        # Save results to a JSON file
        with open('erc1155_transactions.json', 'w') as f:
            json.dump(erc1155_transactions, f, indent=4)
        
        print(f"Extracted {len(erc1155_transactions)} ERC-1155 transactions. Saved to 'erc1155_transactions.json'.")
    else:
        print(f"Error: {data['message']}")
else:
    print(f"HTTP Error: {response.status_code}")