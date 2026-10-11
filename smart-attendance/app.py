from flask import Flask, render_template_string, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head><title>Smart Attendance</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>Smart Attendance System</h1>
            <button onclick="mark()" style="padding: 15px 30px; font-size: 18px; background: green; color: white; border: none; cursor: pointer;">
                Mark Attendance (STU12345)
            </button>
            <p id="msg" style="margin-top: 20px; font-weight: bold;"></p>
            <script>
                function mark() {
                    fetch('/mark', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ student_id: 'STU12345' })
                    })
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('msg').innerText = data.message;
                        document.getElementById('msg').style.color = 'green';
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/mark', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (student_id, timestamp) VALUES (?, ?)", (student_id, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Attendance logged for {student_id} at {timestamp}!"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)