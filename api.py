from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Функция для подключения к базе данных SQLite
def connect_db():
    try:
        conn = sqlite3.connect('users.db')
        print("Database connected successfully")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Маршрут для обработки постбека от 1WIN
@app.route('/postback', methods=['POST'])
def postback():
    # Получаем user_id из POST-запроса
    user_id = request.form.get('user_id')

    # Проверка, передан ли user_id
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    # Добавление user_id в базу данных
    try:
        conn = connect_db()
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()

        # Проверяем, существует ли запись с таким user_id
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()

        if row:
            # Если запись существует, обновляем partnerid
            cursor.execute('''
                UPDATE users SET partnerid = ? WHERE user_id = ?
            ''', (user_id, user_id))
        else:
            # Если записи нет, создаем новую запись
            cursor.execute('''
                INSERT INTO users (user_id, partnerid) VALUES (?, ?)
            ''', (user_id, user_id))

        conn.commit()
        conn.close()

        print(f"Successfully added/updated user_id {user_id} in the database")
        return jsonify({'message': f'Successfully added/updated user_id {user_id} in the database'}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Запуск Flask API
    app.run(debug=True)
