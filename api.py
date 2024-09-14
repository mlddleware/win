from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Получаем порт и параметры подключения из переменных окружения
port = int(os.environ.get("PORT", 5000))
db_url = os.environ.get("DATABASE_URL")

def get_db():
    conn = psycopg2.connect(db_url)
    return conn

@app.route('/postback', methods=['POST'])
def postback():
    user_id = request.form.get('user_id')
    if user_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET partnerid = %s WHERE user_id = %s", (user_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "user_id is required"}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
