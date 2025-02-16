"""
This script processes SMS data from an XML file containing transaction information.

It performs the following steps:
1. Parses an XML file to extract relevant transaction data.
2. Categorizes each transaction based on the body of the SMS.
3. Sets up an SQLite database if it doesn't exist.
4. Inserts the categorized transaction data into the SQLite database.

Modules used:
- xml.etree.ElementTree: To parse XML data.
- sqlite3: To interact with SQLite database.
- re: To use regular expressions for text matching.
- os: To handle file paths.
"""

import xml.etree.ElementTree as ET
import sqlite3
import re
import os

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
    amount = int(re.sub(r'\D', '', amount_match.group(1))) if amount_match else None
    
    if "received" in body:
        return "Incoming Money", ("Incoming Money", amount, date, body)
    if "payment" in body:
        return "Payments", ("Payments", amount, date, body)
    if "transferred" in body:
        return "Transfers", ("Transfers", amount, date, body)
    if "deposit" in body:
        return "Bank Deposits", ("Bank Deposits", amount, date, body)
    if "airtime" in body:
        return "Airtime Bill Payments", ("Airtime", amount, date, body)
    if "withdrawn" in body:
        return "Withdrawals", ("Withdrawals", amount, date, body)
    else:
        return None, None

# Database setup
def setup_database():
    """
    Sets up the database by creating a table for transactions if it does not exist.

    Creates a connection to the 'momo_transactions.db' database and executes a SQL query to create a table named 'transactions' with the following columns:
    - id (INTEGER PRIMARY KEY AUTOINCREMENT)
    - category (TEXT)
    - amount (INTEGER)
    - date (TEXT)
    - description (TEXT)

    Returns:
        None
    """
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
    """
    Inserts a list of transactions into the database.

    Args:
        transactions (list): A list of tuples containing the transaction data.
            Each tuple should contain the category, amount, date, and description of the transaction.

    Returns:
        None
    """
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
    xml_file_path = os.path.join(os.path.dirname(__file__), "modified_sms_v2.xml")  # Renamed variable
    parsed_transactions = parse_xml(xml_file_path)  # Renamed variable
    insert_data(parsed_transactions)  # Use the renamed variable here
    print("Data processing complete.")
