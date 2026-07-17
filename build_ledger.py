pip install requests
import psycopg2
import requests
import json

def fetch_live_crypto_metrics():
    """
    BUSINESS PURPOSE: Programmatically calls public Web3 data infrastructure.
    Maps to Coinbase & Amazon Mandates: 'Safely ingest high-velocity data streams'
    """
    print("Initiating cloud handshake with CoinGecko API network...")
    # Public endpoint tracking live Bitcoin and Ethereum prices in USD
    url = "https://coingecko.com"
    
    try:
        response = requests.get(url, timeout=10)
        # Parse raw web text string into an organized business data dictionary
        market_snapshot = response.json()
        return market_snapshot
    except Exception as network_error:
        print(f"CRITICAL LOSS OF CONNECTION: Cloud API endpoint unreachable: {network_error}")
        return None

def process_and_load_to_ledger(data_payload):
    """
    BUSINESS PURPOSE: Parses unstructured web payloads and commits them to the asset database.
    """
    if not data_payload:
        print("Data payload is empty. Halting operation to prevent database corruption.")
        return

    try:
        # Open connection to our active local Conda database vault
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="",  # Blank to match our trusted local server setup
            database="financial_ledger",
            port="5432"
        )
        cursor = conn.cursor()

        # Extract values like an accountant processing invoices
        btc_usd = float(data_payload['bitcoin']['usd'])
        eth_usd = float(data_payload['ethereum']['usd'])

        # SQL commands to record this data into our Project 1 Ledger
        insert_query = """
        INSERT INTO ledger_transactions (account_id, amount_delta, currency_ticker) 
        VALUES ('ACC_001', %s, %s);
        """

        # Execute inserts securely to prevent SQL injection hacks (Vital for Banks)
        cursor.execute(insert_query, (btc_usd, 'BTC'))
        cursor.execute(insert_query, (eth_usd, 'ETH'))
        
        # Commit saves the transactions permanently to the disk
        conn.commit()
        print(f"SUCCESS: Ingested Cloud Market Rates. BTC: ${btc_usd} | ETH: ${eth_usd}")

        cursor.close()
        conn.close()

    except Exception as db_error:
        print(f"OPERATIONAL EXCEPTION: Ledger database rejected transaction: {db_error}")

if __name__ == "__main__":
    raw_data = fetch_live_crypto_metrics()
    process_and_load_to_ledger(raw_data)

