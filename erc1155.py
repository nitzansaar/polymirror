import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

# API endpoint and parameters
url = "https://api.polygonscan.com/api"
params = {
    "module": "account",
    "action": "token1155tx",
    "address": "0x56687bf447db6ffa42ffe2204a05edaa20f55839",
    "page": 1,
    "offset": 100,
    "startblock": 0,
    "endblock": 99999999,
    "sort": "desc",
    "apikey": os.getenv('POLYGONSCAN_API_KEY'),
}

# Make API request
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if data["status"] == "1":  # API response success
        transactions = data["result"]
        
        print(f"Total ERC1155 transactions found: {len(transactions)}")
        
        # Create list to store transaction data
        transactions_data = []
        
        # Extract transaction data
        for tx in transactions:
            transaction = {
                "transaction_hash": tx["hash"],
                "to": tx["to"],
                "amount": f"{tx['tokenValue']} ERC1155",
                "token": f"ERC1155 Token (ID: {tx['tokenID']})",
                "timestamp": datetime.fromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S'),
                "contract_address": tx["contractAddress"]
            }
            transactions_data.append(transaction)
            
        # Write to JSON file
        with open('erc1155_transactions.json', 'w') as f:
            json.dump(transactions_data, f, indent=4)
    else:
        print(f"Error: {data['message']}")
else:
    print(f"HTTP Error: {response.status_code}")