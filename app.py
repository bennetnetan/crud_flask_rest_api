from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        conn.commit()

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if 'name' not in data:
        return jsonify({'error': 'Task name is required'}), 400

    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (name) VALUES (?)", (data['name'],))
        task_id = cursor.lastrowid
        conn.commit()
        response = {'id': task_id, 'name': data['name']}
    return jsonify(response), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM tasks")
        tasks = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    if 'name' not in data:
        return jsonify({'error': 'Task name is required'}), 400

    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET name = ? WHERE id = ?", (data['name'], task_id))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        conn.commit()
    return jsonify({'id': task_id, 'name': data['name']})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
        conn.commit()
    return jsonify({'message': 'Task deleted'})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)