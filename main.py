from flask import Flask, jsonify, request
import os
import psycopg2

app = Flask(__name__)

# Подключение к БД через переменную окружения
conn = None

def connect_db():
    global conn
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        return  # Для локального теста без БД
    try:
        conn = psycopg2.connect(db_url)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL,
                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    except Exception as e:
        print(f"DB connection error: {e}")

connect_db()

@app.route('/')
def hello():
    return "Hello, Serverless! 🚀\n"

@app.route('/save', methods=['POST'])
def save_message():
    if not conn:
        return jsonify({"error": "Database not connected"}), 500
    
    data = request.get_json()
    message = data.get('message') if data else None
    if not message:
        return jsonify({"error": "No 'message' field in JSON"}), 400

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO messages (text) VALUES (%s)", (message,))
            conn.commit()
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/messages')
def get_messages():
    if not conn:
        return jsonify({"error": "Database not connected"}), 500
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text, time FROM messages ORDER BY time DESC")
            rows = cur.fetchall()
        messages = [{"id": r[0], "text": r[1], "time": str(r[2])} for r in rows]
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)