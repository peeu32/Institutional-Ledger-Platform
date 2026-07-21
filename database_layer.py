"""
MODULE 1: ENTERPRISE DATABASE ARCHITECTURE LAYER
BUSINESS PURPOSE: Manages relational engine handshakes and connection handles.
"""
import psycopg2

def get_warehouse_connection():
    """Establishes an isolated binary connection to the local database cluster."""
    return psycopg2.connect(
        host="localhost",
        user="postgres",
        password="", # Trusted Conda channel local authentication port
        database="financial_ledger",
        port="5432"
    )
