from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("momo_transactions.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/transactions", methods=["GET"])
def get_transactions():
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions").fetchall()
    conn.close()
    return jsonify([dict(tx) for tx in transactions])

@app.route("/transactions/<category>", methods=["GET"])
def get_transactions_by_category(category):
    conn = get_db_connection()
    transactions = conn.execute("SELECT * FROM transactions WHERE category = ?", (category,)).fetchall()
    conn.close()
    return jsonify([dict(tx) for tx in transactions])

if __name__ == "__main__":
    app.run(debug=True)
