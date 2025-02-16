import xml.etree.ElementTree as ET
import sqlite3
import re
import os
from datetime import datetime

# Load and parse the XML file
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    transactions = []
    
    for sms in root.findall('sms'):
        body = sms.get('body')
        if not body:
            continue
        
        transaction_type, details = categorize_transaction(body)
        if transaction_type:
            transactions.append(details)
    
    return transactions

# Categorize transactions
def categorize_transaction(body):
    """
    Categorize a transaction based on the SMS body.

    Args:
        body (str): The SMS body to categorize.

    Returns:
        tuple: A tuple containing the transaction type and details. For example:
            ("Incoming Money", ("Incoming Money", amount, date, body))
    """
    body = body.lower()
    date_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', body)
    date = date_match.group(1) if date_match else None
    amount_match = re.search(r'(\d+\s*rwf)', body)
    amount = int(amount_match.group(1).replace(' rwf', '')) if amount_match else None
    
    if "received" in body:
        return "Incoming Money", ("Incoming Money", amount, date, body)
    elif "payment" in body:
        return "Payments", ("Payments", amount, date, body)
    elif "transferred" in body:
        return "Transfers", ("Transfers", amount, date, body)
    elif "deposit" in body:
        return "Bank Deposits", ("Bank Deposits", amount, date, body)
    elif "airtime" in body:
        return "Airtime Bill Payments", ("Airtime", amount, date, body)
    elif "withdrawn" in body:
        return "Withdrawals", ("Withdrawals", amount, date, body)
    else:
        return None, None

# Database setup
def setup_database():
    conn = sqlite3.connect("momo_transactions.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount INTEGER,
            date TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert data into database
def insert_data(transactions):
    conn = sqlite3.connect("momo_transactions.db")
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO transactions (category, amount, date, description)
        VALUES (?, ?, ?, ?)
    ''', transactions)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    file_path = os.path.join(os.path.dirname(__file__), "modified_sms_v2.xml")
    transactions = parse_xml(file_path)
    insert_data(transactions)
    print("Data processing complete.")
