from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Получаем порт из переменных окружения, установленных Render
port = int(os.environ.get("PORT", 5000))

# Соединение с базой данных SQLite
DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/postback', methods=['POST'])
def postback():
    user_id = request.form.get('user_id')
    if user_id:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET partnerid = ? WHERE user_id = ?", (user_id, user_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "user_id is required"}), 400

if __name__ == "__main__":
    # Запуск приложения на всех интерфейсах и порту, указанном в переменных окружения
    app.run(host='0.0.0.0', port=port)
