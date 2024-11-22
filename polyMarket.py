from dotenv import load_dotenv
import os
from py_clob_client.client import ClobClient
import json

# Load environment variables
load_dotenv()

# Initialize Polymarket CLOB Client
host = "https://clob.polymarket.com"
key = os.getenv("PK")  # Your private key
chain_id = 137  # Polygon Mainnet

client = ClobClient(host, key=key, chain_id=chain_id)
client.set_api_creds(client.create_or_derive_api_creds())

# List of token IDs
token_ids = [
    "15689933950391663206664315906845711271853045861507143124541398615962179259380", 
    # Add more token IDs here
]

# Loop through token IDs and fetch market details
for token_id in token_ids:
    print(f"Fetching market details for Token ID: {token_id}")
    try:
        order_book = client.get_order_book(token_id=token_id)
        market_id = order_book.market
        print(f"Market ID for Token ID {token_id}: {market_id}")
        
        market_details = client.get_market(condition_id=market_id)
        
        # Filter tokens to only include the matching token_id
        matching_token = next(
            (token for token in market_details['tokens'] if token['token_id'] == token_id),
            None
        )
        
        if matching_token:
            # Create new simplified output structure
            output_data = {
                "question": market_details['question'],
                "question_id": market_details['question_id'],
                "active": market_details['active'],
                "closed": market_details['closed'],
                "neg_risk": market_details['neg_risk'],
                "icon": market_details['icon'],
                "image": market_details['image'],
                "price": matching_token['price'],
                "winner": matching_token['winner']
            }
            
            with open('order_book.json', 'w') as f:
                json.dump(output_data, f, indent=4)
        print("-" * 50)
    except Exception as e:
        print(f"Error fetching details for Token ID {token_id}: {e}")

print("Done!")