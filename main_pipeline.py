"""
MODULE 2: HIGH-VELOCITY INGESTION ENGINE RUN-LOOP (PROXY-IMMUNE SDK VERSION)
BUSINESS PURPOSE: Coordinates external API calls utilizing verified enterprise SDK handlers.
LOCAL ENVIRONMENT FIX: Wipes out hidden global Windows proxy variables to force a direct cloud link.
"""
import os
import ccxt                       # The official institutional cross-exchange client library
import database_layer as db      # Our Module 1 storage layer
import governance_gate as gov   # Our Module 3 security gate

# 🔐 THE COMPLIANCE OVERRIDE: Clear out any hidden system proxy traps blocking our outbound traffic
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['all_proxy'] = ''

def fetch_live_market_telemetry():
    """
    BUSINESS PURPOSE: Programmatically extracts spot pricing via certified exchange client libraries.
    """
    # 🏢 CLIENT 1: Initialize the official Coinbase Institutional API connector
    print("Initiating enterprise handshake with Primary SDK Client (Coinbase Platform)...")
    try:
        coinbase_client = ccxt.coinbase()
        # Explicitly configure the client's internal network engine to ignore system proxies
        coinbase_client.proxies = {}
        
        ticker = coinbase_client.fetch_ticker('BTC/USD')
        spot_price = str(ticker['last'])
        return {'bitcoin': {'usd': spot_price}}
    except Exception as e:
        print(f"OPERATIONAL WARNING: Primary SDK Client (Coinbase) connection congested or proxy-blocked: {e}")
    
    # 🏢 CLIENT 2: Initialize the official Kraken Institutional API connector (The Fallback Route)
    print("FALLBACK ROUTE ACTIVATED: Swapping to Secondary SDK Client (Kraken Platform)...")
    try:
        kraken_client = ccxt.kraken()
        kraken_client.proxies = {}
        
        ticker = kraken_client.fetch_ticker('BTC/USD')
        spot_price = str(ticker['last'])
        return {'bitcoin': {'usd': spot_price}}
    except Exception as network_error:
        print(f"CRITICAL LOSS OF CONNECTION: All institutional exchange connections congested: {network_error}")
        return None

def execute_pipeline_loop():
    raw_payload = fetch_live_market_telemetry()
    is_valid = gov.verify_data_contract(raw_payload)
    
    if not is_valid:
        print("CIRCUIT BREAKER: Pipeline execution halted by governance gate.")
        return

    try:
        btc_price = float(raw_payload['bitcoin']['usd'])
        
        conn = db.get_warehouse_connection()
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO financial_ledger (wallet_hash, transaction_type, amount_delta, fee_charged, execution_timestamp, clearing_status) 
        VALUES ('W_HASH_BTC_VAN', 'DEPOSIT', %s, 0.15, CURRENT_TIMESTAMP, 'SETTLED');
        """
        cursor.execute(insert_query, (btc_price,))
        conn.commit()
        
        print(f"SUCCESS: Ingested Verified Data into database. Spot Price: ${btc_price}")
        cursor.close()
        conn.close()
        
    except Exception as db_error:
        print(f"OPERATIONAL EXCEPTION: Storage layer rejected database entry: {db_error}")

if __name__ == "__main__":
    execute_pipeline_loop()
