from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Получаем порт и параметры подключения из переменных окружения
port = int(os.environ.get("PORT", 5000))
db_url = os.environ.get("DATABASE_URL")

def get_db():
    # Устанавливаем подключение к базе данных PostgreSQL
    conn = psycopg2.connect(db_url)
    return conn

@app.route('/postback', methods=['GET', 'POST'])
def postback():
    # Получаем параметры из запроса
    user_id = request.args.get('user_id') if request.method == 'GET' else request.form.get('user_id')
    amount = request.args.get('amount') if request.method == 'GET' else request.form.get('amount')
    
    if user_id:
        # Подключаемся к базе данных
        conn = get_db()
        cursor = conn.cursor()

        # Проверяем, существует ли запись с указанным user_id
        cursor.execute("SELECT 1 FROM users WHERE user_id = %s", (user_id,))
        exists = cursor.fetchone()

        if exists:
            # Если запись существует, обновляем только partner_id и amount
            cursor.execute("UPDATE users SET partner_id = %s, amount = %s WHERE user_id = %s", (user_id, amount, user_id))
        else:
            # Если записи не существует, создаем новую с user_id, partner_id и amount
            cursor.execute("INSERT INTO users (user_id, partner_id, amount) VALUES (%s, %s, %s)", (user_id, user_id, amount))
        
        # Сохраняем изменения в базе данных
        conn.commit()

        # Закрываем соединение
        cursor.close()
        conn.close()

        return jsonify({"status": "success"}), 200

    return jsonify({"status": "error", "message": "user_id is required"}), 400

if __name__ == "__main__":
    # Запуск приложения Flask
    app.run(host='0.0.0.0', port=port)
