from flask import Flask, render_template, jsonify
import sqlite3
import random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('lotto.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lotto (id INTEGER PRIMARY KEY, numbers TEXT)''')
    conn.commit()
    conn.close()

@app.before_first_request
def before_first_request():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate_numbers():
    frequency = [0] * 46
    for _ in range(100):
        numbers = random.sample(range(1, 46), 6)
        for number in numbers:
            frequency[number] += 1

    most_frequent = sorted(range(1, 46), key=lambda i: -frequency[i])[:3]
    least_frequent = sorted(range(1, 46), key=lambda i: frequency[i] if frequency[i] != 0 else float('inf'))[:3]

    data = {
        'frequency': frequency,
        'mostFrequent': most_frequent,
        'leastFrequent': least_frequent
    }
    return jsonify(data)

def generate_lotto_numbers():
    return random.sample(range(1, 46), 6)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
