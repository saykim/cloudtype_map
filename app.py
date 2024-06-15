from flask import Flask, render_template, jsonify
import sqlite3
import random

app = Flask(__name__)

# 데이터베이스 초기화 함수
def init_db():
    conn = sqlite3.connect('lotto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lotto (id INTEGER PRIMARY KEY, numbers TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate_numbers():
    numbers = generate_lotto_numbers()
    conn = sqlite3.connect('lotto.db')
    c = conn.cursor()
    c.execute("INSERT INTO lotto (numbers) VALUES (?)", (','.join(map(str, numbers)),))
    conn.commit()
    conn.close()
    return jsonify({'numbers': numbers})

@app.route('/history', methods=['GET'])
def get_history():
    conn = sqlite3.connect('lotto.db')
    c = conn.cursor()
    c.execute("SELECT * FROM lotto")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

def generate_lotto_numbers():
    return random.sample(range(1, 46), 6)

if __name__ == '__main__':
    init_db()  # 데이터베이스 초기화
    app.run(debug=True, host='0.0.0.0', port=8000)
