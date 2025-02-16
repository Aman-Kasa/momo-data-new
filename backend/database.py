import sqlite3

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
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
