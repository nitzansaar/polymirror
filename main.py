"""
This script monitors transactions from top Polymarket traders by:
1. Fetching token transactions for specific wallet addresses
2. Filtering for transactions sent to the Polymarket contract
3. Displaying transaction details including amount, token, and timestamp
"""


import requests
from datetime import datetime 

# Top dog addresses
addresses = [
    "0x56687bf447db6ffa42ffe2204a05edaa20f55839", 
    "0x1f2dd6d473f3e824cd2f8a89d9c69fb96f6ad0cf", 
    "0x78b9ac44a6d7d7a076c14e0ad518b301b63c6b76"
]


# Define API endpoint and parameters
url = "https://api.polygonscan.com/api"
params = {
    "module": "account",
    "action": "tokentx",
    "address": addresses[2],  # Top dog address
    "startblock": 0,
    "endblock": 99999999,
    "page": 1,
    "offset": 100,  # Adjust to fetch more transactions per page
    "sort": "desc",  # Fetch the most recent transactions first
    "apikey": "QWBM6IIDNGC3GX5ZPJD4PFEZB1X7YSJ4EB", 
}

# Polymarket contract address to filter
polymarket_address = "0xC5d563A36AE78145C45a50134d48A1215220f80a"

# Fetch transactions
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if data["status"] == "1":  # API response success
        transactions = data["result"]

        # Filter transactions sent to Polymarket
        polymarket_transactions = [
            tx for tx in transactions if tx["to"].lower() == polymarket_address.lower()
        ]

        # Print relevant details
        for tx in polymarket_transactions:
            amount = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))
            timestamp = datetime.fromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S')  # Convert timestamp here
            print(f"Transaction Hash: {tx['hash']}")
            print(f"To: {tx['to']}")
            print(f"Amount: {amount} {tx['tokenSymbol']}")
            print(f"Token: {tx['tokenName']}")
            print(f"TimeStamp: {timestamp}")  # Print converted timestamp
            print("-" * 40)
    else:
        print(f"Error: {data['message']}")
else:
    print(f"HTTP Error: {response.status_code}")